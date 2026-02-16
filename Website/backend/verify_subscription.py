#!/usr/bin/env python3
"""
Verify that subscription endpoint is working and sending emails
"""

import sys
import json
import requests
from pathlib import Path

API_URL = "http://localhost:8000/api/subscribe"

print("="*70)
print("SUBSCRIPTION VERIFICATION")
print("="*70)

# Check if backend is running
print("\n1. Checking if backend is running...")
try:
    health = requests.get("http://localhost:8000/api/health", timeout=2)
    if health.status_code == 200:
        print("   ✓ Backend is running")
    else:
        print(f"   ⚠ Backend responded with status {health.status_code}")
except Exception as e:
    print(f"   ❌ Backend is NOT running: {e}")
    print("   → Start backend with: python email_handler.py")
    sys.exit(1)

# Get test email
print("\n2. Enter test email address:")
test_email = input("   Email: ").strip()

if not test_email:
    print("   No email provided. Exiting.")
    sys.exit(1)

# Subscribe
print(f"\n3. Subscribing {test_email}...")
try:
    response = requests.post(
        API_URL,
        json={"email": test_email},
        headers={"Content-Type": "application/json"},
        timeout=15  # Longer timeout for email sending
    )
    
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Subscription Response:")
        print(f"     Success: {data.get('success')}")
        print(f"     Message: {data.get('message')}")
        print(f"     Email: {data.get('email')}")
        
        print("\n" + "="*70)
        print("NEXT STEPS:")
        print("="*70)
        print("1. Check the backend server terminal for email sending logs")
        print("2. Look for messages like:")
        print("   - 'Attempting to send welcome email to...'")
        print("   - '✓ Welcome email sent successfully'")
        print("   - '✗ Failed to send welcome email' (if there's an error)")
        print(f"3. Check {test_email} inbox (and spam folder)")
        print("\nIf email not received, check backend logs for errors")
        
    else:
        print(f"   ❌ Subscription failed!")
        try:
            error = response.json()
            print(f"   Error: {error.get('detail', error)}")
        except:
            print(f"   Error: {response.text}")
            
except requests.exceptions.Timeout:
    print("   ⚠ Request timed out - email sending may be taking longer")
    print("   Check backend logs to see if email was sent")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*70)









