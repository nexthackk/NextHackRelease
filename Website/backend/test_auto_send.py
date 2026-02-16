#!/usr/bin/env python3
"""
Test script to verify automatic email sending on subscription
"""

import requests
import json
import time

API_URL = "http://localhost:8000/api/subscribe"

print("="*70)
print("TESTING AUTOMATIC EMAIL SENDING")
print("="*70)

# Get test email
test_email = input("\nEnter test email address: ").strip()

if not test_email:
    print("No email provided. Exiting.")
    exit(1)

print(f"\n1. Subscribing {test_email}...")
print("   (This should automatically send welcome email)")

try:
    start_time = time.time()
    response = requests.post(
        API_URL,
        json={"email": test_email},
        headers={"Content-Type": "application/json"},
        timeout=30  # Longer timeout for email sending
    )
    elapsed_time = time.time() - start_time
    
    print(f"\n2. Response received in {elapsed_time:.2f} seconds")
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n3. Response Data:")
        print(f"   Success: {data.get('success')}")
        print(f"   Message: {data.get('message')}")
        print(f"   Email: {data.get('email')}")
        
        # Check message for email status
        message = data.get('message', '')
        if 'welcome message' in message.lower() or 'check your email' in message.lower():
            print(f"\n✓ Email sending was attempted!")
            print(f"   Message indicates email should have been sent")
        elif 'could not be sent' in message.lower():
            print(f"\n✗ Email sending failed!")
            print(f"   Check backend logs for details")
        else:
            print(f"\n⚠ Could not determine email status from message")
        
        print("\n" + "="*70)
        print("NEXT STEPS:")
        print("="*70)
        print("1. Check backend server terminal for email sending logs")
        print("2. Look for these messages:")
        print("   - '[BACKEND] Attempting to send welcome email to...'")
        print("   - '[EMAIL SERVICE] ✓ Email sent to...'")
        print("   - '[BACKEND] ✓ Welcome email sent successfully'")
        print(f"3. Check {test_email} inbox (and spam folder)")
        print("4. Email should arrive within 1-5 minutes")
        
    else:
        print(f"\n✗ Subscription failed!")
        try:
            error = response.json()
            print(f"   Error: {error.get('detail', error)}")
        except:
            print(f"   Error: {response.text}")
            
except requests.exceptions.ConnectionError:
    print("\n✗ ERROR: Backend server is not running!")
    print("   Start it with: python email_handler.py")
except requests.exceptions.Timeout:
    print("\n⚠ Request timed out")
    print("   Email sending may be taking longer than expected")
    print("   Check backend logs to see if email was sent")
except Exception as e:
    print(f"\n✗ Error: {e}")

print("\n" + "="*70)









