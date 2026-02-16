#!/usr/bin/env python3
"""
Test script to verify the full subscription flow including email sending
"""

import sys
import requests
import json
from pathlib import Path

# Test configuration
API_BASE_URL = "http://localhost:8000/api"
TEST_EMAIL = input("Enter test email address: ").strip()

if not TEST_EMAIL:
    print("No email provided. Exiting.")
    sys.exit(1)

print("\n" + "="*70)
print("TESTING SUBSCRIPTION FLOW")
print("="*70)

# Test 1: Check if backend is running
print("\n1. Checking if backend server is running...")
try:
    response = requests.get(f"{API_BASE_URL.replace('/api', '')}/api/health", timeout=2)
    if response.status_code == 200:
        print("   ✓ Backend server is running")
    else:
        print(f"   ⚠ Backend responded with status {response.status_code}")
except requests.exceptions.ConnectionError:
    print("   ❌ Backend server is NOT running!")
    print("   → Start it with: python email_handler.py")
    sys.exit(1)
except Exception as e:
    print(f"   ⚠ Error checking backend: {e}")

# Test 2: Subscribe
print(f"\n2. Subscribing {TEST_EMAIL}...")
try:
    response = requests.post(
        f"{API_BASE_URL}/subscribe",
        json={"email": TEST_EMAIL},
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    
    print(f"   Response status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Subscription successful!")
        print(f"   Message: {data.get('message', 'N/A')}")
        print(f"   Email: {data.get('email', 'N/A')}")
        
        print("\n" + "="*70)
        print("NEXT STEPS")
        print("="*70)
        print(f"1. Check the backend server logs for email sending status")
        print(f"2. Check {TEST_EMAIL} inbox (and spam folder) for welcome email")
        print(f"3. If email not received, check backend logs for errors")
        print("\nTo view backend logs, look at the terminal running email_handler.py")
        
    else:
        print(f"   ❌ Subscription failed!")
        try:
            error_data = response.json()
            print(f"   Error: {error_data.get('detail', 'Unknown error')}")
        except:
            print(f"   Error: {response.text}")
            
except requests.exceptions.Timeout:
    print("   ❌ Request timed out - backend may be slow or unresponsive")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*70)









