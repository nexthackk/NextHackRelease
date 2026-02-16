#!/usr/bin/env python3
"""
Check which .env file is being loaded and what values are being used
"""

import os
from pathlib import Path

print("="*70)
print("ENVIRONMENT VARIABLE CHECK")
print("="*70)

# Check .env files
backend_env = Path(__file__).parent / ".env"
parent_env = Path(__file__).parent.parent / ".env"

print(f"\n1. .env file locations:")
print(f"   Backend .env: {backend_env} ({'EXISTS' if backend_env.exists() else 'NOT FOUND'})")
print(f"   Parent .env: {parent_env} ({'EXISTS' if parent_env.exists() else 'NOT FOUND'})")

# Check which one would be loaded
if backend_env.exists():
    print(f"\n2. Backend .env file contents:")
    with open(backend_env, 'r') as f:
        for line in f:
            if 'PASSWORD' in line:
                parts = line.split('=')
                if len(parts) == 2:
                    print(f"   {parts[0]}=***HIDDEN***")
                else:
                    print(f"   {line.strip()}")
            else:
                print(f"   {line.strip()}")

# Check what Python would load
print(f"\n3. Testing email_service import:")
try:
    from email_service import SMTP_USER, SMTP_PASSWORD, SMTP_FROM_EMAIL, SMTP_HOST, SMTP_PORT
    
    print(f"   SMTP_USER: {SMTP_USER}")
    print(f"   SMTP_PASSWORD: {'SET (' + str(len(SMTP_PASSWORD)) + ' chars)' if SMTP_PASSWORD else 'NOT SET'}")
    print(f"   SMTP_FROM_EMAIL: {SMTP_FROM_EMAIL}")
    print(f"   SMTP_HOST: {SMTP_HOST}")
    print(f"   SMTP_PORT: {SMTP_PORT}")
    
    print(f"\n4. Current working directory: {os.getcwd()}")
    print(f"   Email service file: {Path(__file__).parent / 'email_service.py'}")
    
except Exception as e:
    print(f"   ERROR: {e}")

print("\n" + "="*70)
print("IMPORTANT:")
print("="*70)
print("If SMTP_USER doesn't match what you see in .env file:")
print("1. The backend server needs to be RESTARTED")
print("2. Make sure you're editing the correct .env file")
print("3. Check for multiple .env files in different directories")









