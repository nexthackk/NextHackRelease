"""
Email Collection API Handler
Stores email addresses for product launch notifications
"""

import json
import os
import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, field_validator

# Configure logging FIRST (before using logger)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to load environment variables from .env file FIRST (before importing email_service)
try:
    from dotenv import load_dotenv
    from pathlib import Path
    # Load .env from backend directory explicitly
    env_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=env_path, override=True)
    logger.info(f"Loaded .env file from: {env_path}")
    # Verify what was loaded
    import os
    smtp_user = os.getenv('SMTP_USER', 'NOT SET')
    logger.info(f"SMTP_USER from .env: {smtp_user}")
    print(f"[EMAIL_HANDLER] Loaded .env - SMTP_USER: {smtp_user}")
except ImportError:
    pass  # python-dotenv not installed, use system env vars
except Exception as e:
    logger.error(f"Error loading .env file: {e}")

# Import email service AFTER loading .env
try:
    # Force reload email_service to pick up new env vars
    import sys
    if 'email_service' in sys.modules:
        del sys.modules['email_service']
    from email_service import send_welcome_email, SMTP_USER as EMAIL_SERVICE_USER
    logger.info(f"Email service imported - SMTP_USER: {EMAIL_SERVICE_USER}")
    print(f"[EMAIL_HANDLER] Email service SMTP_USER: {EMAIL_SERVICE_USER}")
except ImportError:
    # Fallback if email_service module not found
    def send_welcome_email(email: str) -> bool:
        logging.warning("Email service not available. Welcome emails disabled.")
        return False
except Exception as e:
    logger.error(f"Error importing email service: {e}")
    def send_welcome_email(email: str) -> bool:
        logging.warning("Email service not available due to import error.")
        return False

# Initialize FastAPI app
app = FastAPI(
    title="SecTool Email Collection API",
    description="API for collecting email addresses for product launch notifications",
    version="1.0.0"
)

# CORS middleware to allow frontend requests
# Read allowed origins from environment variable (comma-separated)
# Example: ALLOWED_ORIGINS=https://nexthack-landing.netlify.app,https://www.nexthack.io
allowed_origins_env = os.getenv('ALLOWED_ORIGINS', '*')
if allowed_origins_env == '*':
    allowed_origins = ["*"]
else:
    allowed_origins = [origin.strip() for origin in allowed_origins_env.split(',')]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "subscribers.db"

# Ensure database directory exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


# ============================================
# Database Initialization
# ============================================
def init_database():
    """Initialize the SQLite database for storing subscribers"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            user_agent TEXT,
            verified BOOLEAN DEFAULT 0,
            notified BOOLEAN DEFAULT 0,
            welcome_email_sent BOOLEAN DEFAULT 0,
            welcome_email_sent_at TIMESTAMP
        )
    """)
    
    # Add welcome_email_sent column if it doesn't exist (for existing databases)
    try:
        cursor.execute("ALTER TABLE subscribers ADD COLUMN welcome_email_sent BOOLEAN DEFAULT 0")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cursor.execute("ALTER TABLE subscribers ADD COLUMN welcome_email_sent_at TIMESTAMP")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Create index for faster lookups
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_email ON subscribers(email)
    """)
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")


# Initialize database on startup
init_database()


# ============================================
# Pydantic Models
# ============================================
class SubscribeRequest(BaseModel):
    email: EmailStr
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Additional email validation"""
        if not v or len(v) > 255:
            raise ValueError('Email must be valid and less than 255 characters')
        return v.lower().strip()


class SubscribeResponse(BaseModel):
    success: bool
    message: str
    email: Optional[str] = None


class SubscriberCountResponse(BaseModel):
    count: int


class SubscriberInfo(BaseModel):
    id: int
    email: str
    subscribed_at: str
    verified: bool


# ============================================
# Database Helper Functions
# ============================================
def get_db_connection():
    """Get a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def email_exists(email: str) -> bool:
    """Check if email already exists in database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM subscribers WHERE email = ?", (email,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def add_subscriber(email: str, ip_address: str = None, user_agent: str = None) -> bool:
    """Add a new subscriber to the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO subscribers (email, ip_address, user_agent, welcome_email_sent)
            VALUES (?, ?, ?, 0)
        """, (email, ip_address, user_agent))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Email already exists
        return False
    finally:
        conn.close()


def mark_welcome_email_sent(email: str) -> bool:
    """Mark welcome email as sent for a subscriber"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE subscribers 
            SET welcome_email_sent = 1, welcome_email_sent_at = CURRENT_TIMESTAMP
            WHERE email = ?
        """, (email,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error marking welcome email as sent: {e}")
        return False
    finally:
        conn.close()


def get_welcome_email_status(email: str) -> dict:
    """Get welcome email status for a subscriber"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT welcome_email_sent, welcome_email_sent_at
            FROM subscribers
            WHERE email = ?
        """, (email,))
        row = cursor.fetchone()
        if row:
            return {
                "sent": bool(row['welcome_email_sent']),
                "sent_at": row['welcome_email_sent_at']
            }
        return None
    except Exception as e:
        logger.error(f"Error getting welcome email status: {e}")
        return None
    finally:
        conn.close()


def get_subscriber_count() -> int:
    """Get total number of subscribers"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM subscribers")
    count = cursor.fetchone()['count']
    conn.close()
    return count


def get_all_subscribers(limit: int = 100, offset: int = 0) -> List[Dict]:
    """Get all subscribers (for admin use)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, email, subscribed_at, verified
        FROM subscribers
        ORDER BY subscribed_at DESC
        LIMIT ? OFFSET ?
    """, (limit, offset))
    
    subscribers = []
    for row in cursor.fetchall():
        subscribers.append({
            'id': row['id'],
            'email': row['email'],
            'subscribed_at': row['subscribed_at'],
            'verified': bool(row['verified'])
        })
    
    conn.close()
    return subscribers


def export_subscribers_to_file() -> str:
    """Export all subscriber emails to a text file"""
    conn = get_db_connection()
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
        
        logger.info(f"Subscriber list exported to: {subscribers_file}")
        return str(subscribers_file)
    except Exception as e:
        logger.error(f"Error exporting subscribers to file: {e}")
        return None


def export_subscribers_to_csv() -> str:
    """Export all subscriber emails to a CSV file"""
    import csv
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT email, subscribed_at, welcome_email_sent
        FROM subscribers
        ORDER BY subscribed_at ASC
    """)
    
    subscribers = cursor.fetchall()
    conn.close()
    
    # Create CSV file
    csv_file = BASE_DIR / "subscribers_list.csv"
    
    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(['Email', 'Subscribed At', 'Welcome Email Sent'])
            # Write data
            for row in subscribers:
                writer.writerow([
                    row['email'],
                    row['subscribed_at'],
                    'Yes' if row.get('welcome_email_sent') else 'No'
                ])
        
        logger.info(f"Subscriber CSV exported to: {csv_file}")
        return str(csv_file)
    except Exception as e:
        logger.error(f"Error exporting subscribers to CSV: {e}")
        return None
    """Export all subscriber emails to a CSV file"""
    import csv
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT email, subscribed_at, welcome_email_sent
        FROM subscribers
        ORDER BY subscribed_at ASC
    """)
    
    subscribers = cursor.fetchall()
    conn.close()
    
    # Create CSV file
    csv_file = BASE_DIR / "subscribers_list.csv"
    
    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(['Email', 'Subscribed At', 'Welcome Email Sent'])
            # Write data
            for row in subscribers:
                writer.writerow([
                    row['email'],
                    row['subscribed_at'],
                    'Yes' if row.get('welcome_email_sent') else 'No'
                ])
        
        logger.info(f"Subscriber CSV exported to: {csv_file}")
        return str(csv_file)
    except Exception as e:
        logger.error(f"Error exporting subscribers to CSV: {e}")
        return None


# ============================================
# API Endpoints
# ============================================
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SecTool Email Collection API",
        "version": "1.0.0",
        "endpoints": {
            "subscribe": "/api/subscribe",
            "count": "/api/subscribers/count",
            "health": "/api/health"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected" if os.path.exists(DB_PATH) else "not_found",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/subscribe", response_model=SubscribeResponse)
async def subscribe(request: SubscribeRequest):
    """
    Subscribe an email address for product launch notifications
    
    - **email**: Valid email address
    """
    email = request.email
    
    # Check if email already exists
    if email_exists(email):
        # Check if welcome email was sent
        email_status = get_welcome_email_status(email)
        if email_status and not email_status.get("sent"):
            # User is subscribed but didn't receive welcome email - send it now
            logger.info(f"Resending welcome email to existing subscriber: {email}")
            print(f"[BACKEND] Resending welcome email to existing subscriber: {email}")
            try:
                email_sent = send_welcome_email(email)
                if email_sent:
                    mark_welcome_email_sent(email)
                    logger.info(f"✓ Welcome email resent successfully to {email}")
                    print(f"[BACKEND] ✓ Welcome email resent successfully to {email}")
                    return SubscribeResponse(
                        success=True,
                        message="🎉 Welcome email sent! Check your inbox for a welcome message.",
                        email=email
                    )
            except Exception as e:
                logger.error(f"Error resending welcome email: {e}")
        
        return SubscribeResponse(
            success=True,
            message="You're already subscribed! We'll notify you when we launch.",
            email=email
        )
    
    # Get client info (optional, for analytics)
    # In production, you might want to get this from request headers
    ip_address = None
    user_agent = None
    
    # Add subscriber to database
    success = add_subscriber(email, ip_address, user_agent)
    
    if success:
        # Export subscribers list to file (update the list)
        try:
            export_subscribers_to_file()
            export_subscribers_to_csv()
            logger.info("Subscriber list files updated")
        except Exception as e:
            logger.warning(f"Failed to update subscriber list files: {e}")
        # Send welcome email immediately and automatically (synchronously to ensure it's sent)
        email_sent = False
        email_error = None
        try:
            logger.info(f"=== AUTOMATIC EMAIL SENDING: Attempting to send welcome email to {email} ===")
            print(f"\n{'='*70}")
            print(f"[AUTO-SEND] User subscribed: {email}")
            print(f"[AUTO-SEND] Sending welcome email automatically...")
            print(f"{'='*70}")
            
            # Verify email service is available
            try:
                from email_service import send_welcome_email, SMTP_USER, SMTP_PASSWORD
                if not SMTP_USER or not SMTP_PASSWORD:
                    logger.error("Email service not configured: SMTP_USER or SMTP_PASSWORD is missing")
                    print(f"[AUTO-SEND] ✗ Email service not configured!")
                    print(f"[AUTO-SEND] SMTP_USER: {SMTP_USER or 'NOT SET'}")
                    print(f"[AUTO-SEND] SMTP_PASSWORD: {'SET' if SMTP_PASSWORD else 'NOT SET'}")
                    email_sent = False
                    email_error = "Email service not configured - check .env file"
                else:
                    email_sent = send_welcome_email(email)
            except ImportError as ie:
                logger.error(f"Failed to import email service: {ie}")
                print(f"[AUTO-SEND] ✗ Failed to import email service: {ie}")
                email_sent = False
                email_error = f"Email service import error: {ie}"
            except Exception as e:
                logger.error(f"Unexpected error in email service: {e}", exc_info=True)
                print(f"[AUTO-SEND] ✗ Unexpected error: {e}")
                email_sent = False
                email_error = str(e)
                raise  # Re-raise to be caught by outer exception handler
            if email_sent:
                # Mark welcome email as sent in database
                mark_welcome_email_sent(email)
                logger.info(f"✓ Welcome email sent successfully to {email}")
                print(f"[AUTO-SEND] ✓ SUCCESS: Welcome email automatically sent to {email}")
                print(f"[AUTO-SEND] Email should arrive in 1-5 minutes")
                print(f"{'='*70}\n")
            else:
                logger.warning(f"✗ Failed to send welcome email to {email} - check email service configuration")
                print(f"[AUTO-SEND] ✗ FAILED: Could not send welcome email to {email}")
                print(f"[AUTO-SEND] Check email configuration in .env file")
                print(f"{'='*70}\n")
                email_error = "Email service configuration issue"
        except Exception as e:
            # Log the full error for debugging
            logger.error(f"✗ Error sending welcome email to {email}: {e}", exc_info=True)
            print(f"[BACKEND] ✗ Error sending welcome email: {e}")  # Console output
            email_error = str(e)
        
        # Return success response with email status
        if email_sent:
            return SubscribeResponse(
                success=True,
                message="🎉 Success! We'll notify you when we launch. Check your email for a welcome message!",
                email=email
            )
        else:
            # Still return success for subscription, but log the email failure
            logger.warning(f"Subscription successful for {email}, but welcome email was not sent: {email_error}")
            return SubscribeResponse(
                success=True,
                message="🎉 Success! You're subscribed. (Note: Welcome email could not be sent - please check email configuration)",
                email=email
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add subscriber. Please try again."
        )


@app.get("/api/subscribers/count", response_model=SubscriberCountResponse)
async def get_count():
    """Get the total number of subscribers"""
    count = get_subscriber_count()
    return SubscriberCountResponse(count=count)


@app.get("/api/subscribers")
async def list_subscribers(limit: int = 100, offset: int = 0):
    """
    Get list of all subscribers (for admin use)
    
    - **limit**: Maximum number of subscribers to return (default: 100)
    - **offset**: Number of subscribers to skip (default: 0)
    """
    subscribers = get_all_subscribers(limit, offset)
    total_count = get_subscriber_count()
    
    return {
        "total": total_count,
        "limit": limit,
        "offset": offset,
        "subscribers": subscribers
    }


# ============================================
# Export Subscribers (Utility Endpoint)
# ============================================
@app.get("/api/subscribers/export")
async def export_subscribers():
    """
    Export all subscriber emails as JSON (for admin use)
    """
    subscribers = get_all_subscribers(limit=10000)  # Large limit for export
    
    export_data = {
        "export_date": datetime.utcnow().isoformat(),
        "total_subscribers": len(subscribers),
        "emails": [sub['email'] for sub in subscribers]
    }
    
    return export_data


@app.get("/api/subscribers/file")
async def get_subscribers_file():
    """
    Get the subscribers list text file
    """
    from fastapi.responses import FileResponse
    
    # Export fresh file
    file_path = export_subscribers_to_file()
    
    if file_path and Path(file_path).exists():
        return FileResponse(
            path=file_path,
            filename="subscribers_list.txt",
            media_type="text/plain"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscribers list file not found. No subscribers yet."
        )


@app.get("/api/subscribers/csv")
async def get_subscribers_csv():
    """
    Get the subscribers list CSV file
    """
    from fastapi.responses import FileResponse
    
    # Export fresh CSV
    csv_path = export_subscribers_to_csv()
    
    if csv_path and Path(csv_path).exists():
        return FileResponse(
            path=csv_path,
            filename="subscribers_list.csv",
            media_type="text/csv"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscribers CSV file not found."
        )


@app.post("/api/resend-welcome")
async def resend_welcome_email(request: SubscribeRequest):
    """
    Resend welcome email to a subscriber
    """
    email = request.email
    
    # Check if email exists
    if not email_exists(email):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found in subscribers list"
        )
    
    # Send welcome email
    try:
        logger.info(f"Resending welcome email to {email}")
        print(f"[BACKEND] Resending welcome email to {email}")
        email_sent = send_welcome_email(email)
        
        if email_sent:
            mark_welcome_email_sent(email)
            return SubscribeResponse(
                success=True,
                message="Welcome email sent! Check your inbox.",
                email=email
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send welcome email. Please check email configuration."
            )
    except Exception as e:
        logger.error(f"Error resending welcome email: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending email: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    print("Starting Email Collection API Server...")
    print(f"Database location: {DB_PATH}")
    print("API will be available at: http://localhost:8000")
    print("API docs available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)

