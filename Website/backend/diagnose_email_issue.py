#!/usr/bin/env python3
"""
Diagnose why email sending might be failing when called from API
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("="*70)
print("EMAIL SERVICE DIAGNOSIS")
print("="*70)

# Test 1: Check if email service can be imported
print("\n1. Testing email service import...")
try:
    from email_service import send_welcome_email, SMTP_USER, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT
    print("   ✓ Email service imported successfully")
except ImportError as e:
    print(f"   ✗ Failed to import email service: {e}")
    sys.exit(1)

# Test 2: Check configuration
print("\n2. Checking email configuration...")
print(f"   SMTP_HOST: {SMTP_HOST}")
print(f"   SMTP_PORT: {SMTP_PORT}")
print(f"   SMTP_USER: {SMTP_USER or 'NOT SET'}")
print(f"   SMTP_PASSWORD: {'SET (' + str(len(SMTP_PASSWORD)) + ' chars)' if SMTP_PASSWORD else 'NOT SET'}")

if not SMTP_USER or not SMTP_PASSWORD:
    print("\n   ✗ ERROR: Email credentials not configured!")
    print("   → Check your .env file")
    sys.exit(1)
else:
    print("   ✓ Email credentials are configured")

# Test 3: Test email sending function directly
print("\n3. Testing email sending function...")
test_email = input("   Enter test email (or press Enter to skip): ").strip()

if test_email:
    try:
        result = send_welcome_email(test_email)
        if result:
            print(f"   ✓ Email sent successfully to {test_email}")
        else:
            print(f"   ✗ Email sending returned False")
            print("   → Check backend logs for error details")
    except Exception as e:
        print(f"   ✗ Exception occurred: {e}")
        import traceback
        traceback.print_exc()
else:
    print("   Skipped (no email provided)")

# Test 4: Check if called from email_handler context
print("\n4. Testing import from email_handler context...")
try:
    # Simulate how email_handler imports it
    import email_handler
    print("   ✓ email_handler module can be imported")
    
    # Check if send_welcome_email is available in email_handler
    if hasattr(email_handler, 'send_welcome_email'):
        print("   ✓ send_welcome_email is available in email_handler")
    else:
        print("   ⚠ send_welcome_email not found in email_handler")
        print("   → This might be the issue - check email_handler imports")
        
except Exception as e:
    print(f"   ✗ Error importing email_handler: {e}")

print("\n" + "="*70)
print("DIAGNOSIS COMPLETE")
print("="*70)
print("\nIf email test works but API fails:")
print("1. Make sure backend server is running: python email_handler.py")
print("2. Check backend terminal for error messages")
print("3. Verify .env file is in the backend directory")
print("4. Check that python-dotenv is installed: pip install python-dotenv")









