#!/usr/bin/env python3
"""
Test script to verify email configuration and sending
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ .env file loaded")
except ImportError:
    print("⚠ python-dotenv not installed. Install with: pip install python-dotenv")
    print("  Using system environment variables instead")

# Import email service
try:
    from email_service import (
        send_welcome_email,
        EMAIL_PROVIDER,
        SMTP_USER,
        SMTP_PASSWORD,
        SMTP_FROM_EMAIL,
        SMTP_FROM_NAME,
        SMTP_HOST,
        SMTP_PORT
    )
    
    print("\n" + "="*60)
    print("EMAIL CONFIGURATION CHECK")
    print("="*60)
    print(f"Email Provider: {EMAIL_PROVIDER}")
    print(f"SMTP Host: {SMTP_HOST}")
    print(f"SMTP Port: {SMTP_PORT}")
    print(f"SMTP User: {SMTP_USER or 'NOT SET'}")
    print(f"SMTP Password: {'SET' if SMTP_PASSWORD else 'NOT SET'}")
    print(f"From Email: {SMTP_FROM_EMAIL or 'NOT SET'}")
    print(f"From Name: {SMTP_FROM_NAME}")
    
    print("\n" + "="*60)
    print("CONFIGURATION STATUS")
    print("="*60)
    
    if not SMTP_USER or not SMTP_PASSWORD:
        print("❌ ERROR: SMTP credentials are not configured!")
        print("\nTo fix this:")
        print("1. Make sure .env file exists in the backend directory")
        print("2. Add the following to .env:")
        print("   SMTP_USER=your-email@gmail.com")
        print("   SMTP_PASSWORD=your-app-password")
        print("   SMTP_FROM_EMAIL=your-email@gmail.com")
        print("   SMTP_FROM_NAME=NextHack Team")
        print("3. Install python-dotenv: pip install python-dotenv")
        sys.exit(1)
    else:
        print("✓ SMTP credentials are configured")
    
    # Test email sending
    print("\n" + "="*60)
    print("TESTING EMAIL SENDING")
    print("="*60)
    
    test_email = input("\nEnter a test email address to send welcome email: ").strip()
    
    if not test_email:
        print("No email provided. Exiting.")
        sys.exit(0)
    
    print(f"\nSending welcome email to {test_email}...")
    print("This may take a few seconds...\n")
    
    try:
        success = send_welcome_email(test_email)
        if success:
            print(f"✓ SUCCESS! Welcome email sent to {test_email}")
            print("  Please check the inbox (and spam folder) for the email.")
        else:
            print(f"❌ FAILED to send email to {test_email}")
            print("  Check the error messages above for details.")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        
except ImportError as e:
    print(f"❌ ERROR: Could not import email_service: {e}")
    print("Make sure email_service.py exists in the backend directory")
    sys.exit(1)









