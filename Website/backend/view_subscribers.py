#!/usr/bin/env python3
"""
View all subscriber emails from the list file
"""

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
subscribers_file = BASE_DIR / "subscribers_list.txt"

print("="*70)
print("NEXTHACK SUBSCRIBER EMAIL LIST")
print("="*70)

if subscribers_file.exists():
    print(f"\nReading from: {subscribers_file}\n")
    with open(subscribers_file, 'r', encoding='utf-8') as f:
        print(f.read())
else:
    print(f"\n⚠ Subscriber list file not found: {subscribers_file}")
    print("  This means no subscribers have been added yet.")
    print("  The file will be created automatically when the first user subscribes.")

print("\n" + "="*70)
print("File location:", subscribers_file)
print("="*70)









