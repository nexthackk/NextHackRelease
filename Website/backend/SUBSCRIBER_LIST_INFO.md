# Subscriber Email List - Automatic Export

## Overview

Every time a user subscribes by clicking "Notify Me", their email is automatically added to a subscriber list file.

## Files Created

### 1. `subscribers_list.txt`
**Location:** `Website1/subscribers_list.txt`

A formatted text file containing:
- Header with generation date and total count
- Numbered list of all subscriber emails
- Subscription dates for each email

**Format:**
```
======================================================================
NEXTHACK - SUBSCRIBER EMAIL LIST
======================================================================
Generated: 2025-11-24 18:07:15
Total Subscribers: 2
======================================================================

EMAIL ADDRESSES:
----------------------------------------------------------------------
1. user1@example.com (Subscribed: 2025-11-24 12:17:55)
2. user2@example.com (Subscribed: 2025-11-24 12:23:53)
======================================================================
END OF LIST
======================================================================
```

### 2. `subscribers_list.csv`
**Location:** `Website1/subscribers_list.csv`

A CSV file with columns:
- Email
- Subscribed At
- Welcome Email Sent

## How It Works

1. User clicks "Notify Me" on the website
2. Email is saved to database
3. **Automatically exports to both files** (text and CSV)
4. Files are updated in real-time

## Viewing the List

### Option 1: View Text File
```bash
cd Website1
cat subscribers_list.txt
```

### Option 2: Use View Script
```bash
cd Website1/backend
python view_subscribers.py
```

### Option 3: Download via API
When backend is running:
- **Text file:** http://localhost:8000/api/subscribers/file
- **CSV file:** http://localhost:8000/api/subscribers/csv

### Option 4: Manual Export
```bash
cd Website1/backend
python test_export.py
```

## File Locations

- **Text file:** `Website1/subscribers_list.txt`
- **CSV file:** `Website1/subscribers_list.csv`
- **Database:** `Website1/subscribers.db`

## Notes

- Files are **automatically updated** when new users subscribe
- Files are created in the `Website1/` directory (parent of backend)
- If no subscribers exist yet, files won't be created until first subscription
- Files are overwritten each time (always contains complete list)

## API Endpoints

- `GET /api/subscribers/file` - Download text file
- `GET /api/subscribers/csv` - Download CSV file
- `GET /api/subscribers/export` - Get JSON export









