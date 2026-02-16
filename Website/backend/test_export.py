#!/usr/bin/env python3
"""
Test subscriber export functionality
"""

import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "subscribers.db"

def export_subscribers_to_file():
    """Export all subscriber emails to a text file"""
    if not DB_PATH.exists():
        print("Database not found. No subscribers to export.")
        return None
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT email, subscribed_at
        FROM subscribers
        ORDER BY subscribed_at ASC
    """)
    
    subscribers = cursor.fetchall()
    conn.close()
    
    # Create subscribers list file
    subscribers_file = BASE_DIR / "subscribers_list.txt"
    
    try:
        with open(subscribers_file, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("NEXTHACK - SUBSCRIBER EMAIL LIST\n")
            f.write("="*70 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Subscribers: {len(subscribers)}\n")
            f.write("="*70 + "\n\n")
            
            if subscribers:
                f.write("EMAIL ADDRESSES:\n")
                f.write("-"*70 + "\n")
                for i, row in enumerate(subscribers, 1):
                    email = row['email']
                    subscribed_at = row['subscribed_at']
                    f.write(f"{i}. {email} (Subscribed: {subscribed_at})\n")
            else:
                f.write("No subscribers yet.\n")
            
            f.write("\n" + "="*70 + "\n")
            f.write("END OF LIST\n")
            f.write("="*70 + "\n")
        
        print(f"✓ Subscriber list exported to: {subscribers_file}")
        print(f"  Total subscribers: {len(subscribers)}")
        return str(subscribers_file)
    except Exception as e:
        print(f"✗ Error exporting subscribers to file: {e}")
        return None

if __name__ == "__main__":
    print("="*70)
    print("EXPORTING SUBSCRIBER EMAIL LIST")
    print("="*70)
    result = export_subscribers_to_file()
    if result:
        print(f"\n✓ File created successfully!")
        print(f"  Location: {result}")
        print(f"\nTo view the list:")
        print(f"  cat {result}")
        print(f"  or")
        print(f"  python view_subscribers.py")









