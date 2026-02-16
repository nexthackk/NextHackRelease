#!/usr/bin/env python3
"""
Script to resend welcome emails to subscribers who didn't receive them
"""

import sys
import sqlite3
from pathlib import Path
from email_service import send_welcome_email

DB_PATH = Path(__file__).parent / "subscribers.db"

def get_subscribers_without_welcome_email():
    """Get all subscribers who haven't received welcome email"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get subscribers where welcome_email_sent is 0 or NULL
    cursor.execute("""
        SELECT email, subscribed_at, welcome_email_sent
        FROM subscribers
        WHERE welcome_email_sent = 0 OR welcome_email_sent IS NULL
        ORDER BY subscribed_at DESC
    """)
    
    subscribers = []
    for row in cursor.fetchall():
        subscribers.append({
            'email': row['email'],
            'subscribed_at': row['subscribed_at'],
            'welcome_email_sent': row['welcome_email_sent']
        })
    
    conn.close()
    return subscribers


def mark_welcome_email_sent(email: str):
    """Mark welcome email as sent"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE subscribers 
        SET welcome_email_sent = 1, welcome_email_sent_at = CURRENT_TIMESTAMP
        WHERE email = ?
    """, (email,))
    conn.commit()
    conn.close()


def main():
    print("="*70)
    print("RESEND WELCOME EMAILS")
    print("="*70)
    
    subscribers = get_subscribers_without_welcome_email()
    
    if not subscribers:
        print("\n✓ All subscribers have received welcome emails!")
        return
    
    print(f"\nFound {len(subscribers)} subscribers without welcome emails:")
    for sub in subscribers:
        print(f"  - {sub['email']} (subscribed: {sub['subscribed_at']})")
    
    print("\n" + "="*70)
    confirm = input("Send welcome emails to all of them? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("Cancelled.")
        return
    
    print("\nSending welcome emails...")
    print("="*70)
    
    success_count = 0
    fail_count = 0
    
    for sub in subscribers:
        email = sub['email']
        print(f"\nSending to {email}...")
        try:
            if send_welcome_email(email):
                mark_welcome_email_sent(email)
                print(f"  ✓ Sent successfully")
                success_count += 1
            else:
                print(f"  ✗ Failed to send")
                fail_count += 1
        except Exception as e:
            print(f"  ✗ Error: {e}")
            fail_count += 1
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"✓ Successfully sent: {success_count}")
    print(f"✗ Failed: {fail_count}")
    print(f"Total: {len(subscribers)}")


if __name__ == "__main__":
    main()









