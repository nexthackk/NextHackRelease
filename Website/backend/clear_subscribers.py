#!/usr/bin/env python3
"""
Clear all subscribers from the database for retesting
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "subscribers.db"

print("="*70)
print("CLEAR ALL SUBSCRIBERS")
print("="*70)

if not DB_PATH.exists():
    print(f"\n✓ Database file not found at {DB_PATH}")
    print("  No subscribers to clear.")
    exit(0)

# Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get count before deletion
cursor.execute("SELECT COUNT(*) FROM subscribers")
count_before = cursor.fetchone()[0]

print(f"\nCurrent subscribers in database: {count_before}")

if count_before == 0:
    print("\n✓ Database is already empty. Nothing to clear.")
    conn.close()
    exit(0)

# Confirm deletion
print("\n" + "="*70)
confirm = input(f"Are you sure you want to delete ALL {count_before} subscribers? (yes/no): ").strip().lower()

if confirm != 'yes':
    print("\nCancelled. No subscribers were deleted.")
    conn.close()
    exit(0)

# Delete all subscribers
print("\nDeleting all subscribers...")
cursor.execute("DELETE FROM subscribers")
conn.commit()

# Verify deletion
cursor.execute("SELECT COUNT(*) FROM subscribers")
count_after = cursor.fetchone()[0]

conn.close()

print("\n" + "="*70)
if count_after == 0:
    print(f"✓ SUCCESS: All {count_before} subscribers have been deleted!")
    print("  Database is now empty and ready for retesting.")
else:
    print(f"⚠ WARNING: Expected 0 subscribers, but found {count_after}")
    print("  Something went wrong. Please check the database manually.")

print("="*70)
print("\nYou can now retest the subscription flow:")
print("1. Start backend: python email_handler.py")
print("2. Open index.html in browser")
print("3. Enter email and click 'Notify Me'")
print("4. Check email inbox for welcome message")









