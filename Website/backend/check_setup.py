#!/usr/bin/env python3
"""
Diagnostic script to check if the email setup is working correctly
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("="*70)
print("NEXTHACK EMAIL SETUP DIAGNOSTIC")
print("="*70)

# 1. Check .env file
print("\n1. Checking .env file...")
env_file = Path(__file__).parent / '.env'
if env_file.exists():
    print(f"   ✓ .env file exists at: {env_file}")
    with open(env_file, 'r') as f:
        content = f.read()
        if 'SMTP_USER' in content and 'SMTP_PASSWORD' in content:
            print("   ✓ .env file contains SMTP credentials")
        else:
            print("   ⚠ .env file exists but may be missing credentials")
else:
    print(f"   ❌ .env file NOT FOUND at: {env_file}")

# 2. Check python-dotenv
print("\n2. Checking python-dotenv installation...")
try:
    import dotenv
    print("   ✓ python-dotenv is installed")
except ImportError:
    print("   ❌ python-dotenv is NOT installed")
    print("   → Install with: pip install python-dotenv")

# 3. Check email service configuration
print("\n3. Checking email service configuration...")
try:
    from email_service import (
        EMAIL_PROVIDER,
        SMTP_USER,
        SMTP_PASSWORD,
        SMTP_FROM_EMAIL,
        SMTP_FROM_NAME,
        SMTP_HOST,
        SMTP_PORT
    )
    
    print(f"   Email Provider: {EMAIL_PROVIDER}")
    print(f"   SMTP Host: {SMTP_HOST}")
    print(f"   SMTP Port: {SMTP_PORT}")
    print(f"   SMTP User: {SMTP_USER or 'NOT SET'}")
    print(f"   SMTP Password: {'SET' if SMTP_PASSWORD else 'NOT SET'}")
    print(f"   From Email: {SMTP_FROM_EMAIL or 'NOT SET'}")
    print(f"   From Name: {SMTP_FROM_NAME}")
    
    if SMTP_USER and SMTP_PASSWORD:
        print("   ✓ Email credentials are configured")
    else:
        print("   ❌ Email credentials are NOT configured")
        print("   → Check your .env file")
        
except ImportError as e:
    print(f"   ❌ Could not import email_service: {e}")

# 4. Test email sending function
print("\n4. Testing email sending function...")
try:
    from email_service import send_welcome_email
    
    # Test with a dummy email (won't actually send)
    print("   Testing email template generation...")
    from email_service import get_welcome_email_template
    template = get_welcome_email_template("test@example.com")
    if template.get("html") and template.get("text"):
        print("   ✓ Email template generation works")
    else:
        print("   ❌ Email template generation failed")
        
except Exception as e:
    print(f"   ❌ Error testing email service: {e}")

# 5. Check backend server
print("\n5. Checking backend server...")
try:
    import requests
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=2)
        if response.status_code == 200:
            print("   ✓ Backend server is running on http://localhost:8000")
        else:
            print(f"   ⚠ Backend server responded with status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ⚠ Backend server is NOT running")
        print("   → Start with: python email_handler.py")
    except Exception as e:
        print(f"   ⚠ Could not check backend server: {e}")
except ImportError:
    print("   ⚠ requests library not installed (optional)")

# 6. Summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)

try:
    from email_service import SMTP_USER, SMTP_PASSWORD
    if SMTP_USER and SMTP_PASSWORD:
        print("✓ Email setup is CONFIGURED and READY")
        print("\nTo test email sending:")
        print("  python test_email.py")
        print("\nTo start the backend server:")
        print("  python email_handler.py")
    else:
        print("❌ Email setup is NOT CONFIGURED")
        print("\nTo fix:")
        print("1. Create a .env file in the backend directory")
        print("2. Add your SMTP credentials (see .env.example)")
        print("3. Install python-dotenv: pip install python-dotenv")
except:
    print("❌ Could not verify email setup")

print("\n" + "="*70)









