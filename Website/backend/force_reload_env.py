#!/usr/bin/env python3
"""
Force reload environment variables to see what's actually being used
"""

import os
import sys
from pathlib import Path

# Clear any existing environment variables
for key in list(os.environ.keys()):
    if key.startswith('SMTP_'):
        del os.environ[key]

# Load from .env file
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    print(f"Loading .env from: {env_path}")
    load_dotenv(dotenv_path=env_path, override=True)
except ImportError:
    print("python-dotenv not installed")
    sys.exit(1)

print("\n" + "="*70)
print("ENVIRONMENT VARIABLES AFTER LOADING .env")
print("="*70)
print(f"SMTP_USER: {os.getenv('SMTP_USER', 'NOT SET')}")
print(f"SMTP_PASSWORD: {'SET (' + str(len(os.getenv('SMTP_PASSWORD', ''))) + ' chars)' if os.getenv('SMTP_PASSWORD') else 'NOT SET'}")
print(f"SMTP_FROM_EMAIL: {os.getenv('SMTP_FROM_EMAIL', 'NOT SET')}")
print(f"SMTP_HOST: {os.getenv('SMTP_HOST', 'NOT SET')}")
print(f"SMTP_PORT: {os.getenv('SMTP_PORT', 'NOT SET')}")

# Now test what email_service would load
print("\n" + "="*70)
print("TESTING EMAIL_SERVICE IMPORT")
print("="*70)

# Clear module cache to force reload
if 'email_service' in sys.modules:
    del sys.modules['email_service']

try:
    from email_service import SMTP_USER, SMTP_PASSWORD, SMTP_FROM_EMAIL
    print(f"SMTP_USER: {SMTP_USER}")
    print(f"SMTP_PASSWORD: {'SET (' + str(len(SMTP_PASSWORD)) + ' chars)' if SMTP_PASSWORD else 'NOT SET'}")
    print(f"SMTP_FROM_EMAIL: {SMTP_FROM_EMAIL}")
    
    if SMTP_USER == 'alastaair66@gmail.com':
        print("\n⚠ WARNING: Still loading alastaair66@gmail.com!")
        print("This means the backend server is using OLD credentials from memory.")
        print("You MUST restart the backend server!")
    elif SMTP_USER == 'contactnexthack@gmail.com':
        print("\n✓ Correct account loaded: contactnexthack@gmail.com")
        print("If backend still uses wrong account, restart the server!")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)









