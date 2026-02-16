#!/usr/bin/env python3
"""
Debug script to test email sending with detailed output
"""

import sys
import logging
from pathlib import Path

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

sys.path.insert(0, str(Path(__file__).parent))

# Import email service
from email_service import (
    send_welcome_email,
    SMTP_USER,
    SMTP_PASSWORD,
    SMTP_FROM_EMAIL,
    SMTP_HOST,
    SMTP_PORT,
    EMAIL_PROVIDER
)

print("="*70)
print("EMAIL SENDING DEBUG")
print("="*70)
print(f"\nConfiguration:")
print(f"  Email Provider: {EMAIL_PROVIDER}")
print(f"  SMTP Host: {SMTP_HOST}")
print(f"  SMTP Port: {SMTP_PORT}")
print(f"  SMTP User: {SMTP_USER}")
print(f"  SMTP Password: {'SET (' + str(len(SMTP_PASSWORD)) + ' chars)' if SMTP_PASSWORD else 'NOT SET'}")
print(f"  From Email: {SMTP_FROM_EMAIL}")

if not SMTP_USER or not SMTP_PASSWORD:
    print("\n❌ ERROR: SMTP credentials not configured!")
    print("Please check your .env file")
    sys.exit(1)

print("\n" + "="*70)
test_email = input("Enter email address to test: ").strip()

if not test_email:
    print("No email provided. Exiting.")
    sys.exit(1)

print(f"\nSending welcome email to {test_email}...")
print("="*70)

try:
    result = send_welcome_email(test_email)
    print("\n" + "="*70)
    if result:
        print("✓ SUCCESS: Email sent successfully!")
        print(f"  Please check {test_email} inbox (and spam folder)")
    else:
        print("✗ FAILED: Email was not sent")
        print("  Check the error messages above for details")
    print("="*70)
except Exception as e:
    print(f"\n✗ EXCEPTION: {e}")
    import traceback
    traceback.print_exc()









