"""
NextHack Email Collection API
SendGrid Production Version
"""

import os
import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, field_validator

# Import SendGrid email function ONLY
from email_service import send_welcome_email


# ======================================================
# Logging
# ======================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ======================================================
# FastAPI Setup
# ======================================================

app = FastAPI(
    title="NextHack Email API",
    version="2.0.0"
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
if allowed_origins == "*":
    origins = ["*"]
else:
    origins = [o.strip() for o in allowed_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ======================================================
# Database Setup
# ======================================================

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "subscribers.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            welcome_email_sent BOOLEAN DEFAULT 0,
            welcome_email_sent_at TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


init_db()


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def email_exists(email: str) -> bool:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM subscribers WHERE email = ?", (email,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists


def add_subscriber(email: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO subscribers (email, welcome_email_sent)
        VALUES (?, 0)
    """, (email,))
    conn.commit()
    conn.close()


def mark_email_sent(email: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE subscribers
        SET welcome_email_sent = 1,
            welcome_email_sent_at = CURRENT_TIMESTAMP
        WHERE email = ?
    """, (email,))
    conn.commit()
    conn.close()


def get_count() -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as count FROM subscribers")
    count = cur.fetchone()["count"]
    conn.close()
    return count


def get_all_subscribers(limit: int = 100, offset: int = 0) -> List[Dict]:
    """
    Return a list of subscribers with basic fields.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            id,
            email,
            subscribed_at,
            welcome_email_sent,
            welcome_email_sent_at
        FROM subscribers
        ORDER BY subscribed_at DESC
        LIMIT ? OFFSET ?
        """,
        (limit, offset),
    )
    rows = cur.fetchall()
    conn.close()

    subscribers: List[Dict] = []
    for row in rows:
        subscribers.append(
            {
                "id": row["id"],
                "email": row["email"],
                "subscribed_at": row["subscribed_at"],
                "welcome_email_sent": bool(row["welcome_email_sent"]),
                "welcome_email_sent_at": row["welcome_email_sent_at"],
            }
        )
    return subscribers


# ======================================================
# Pydantic Models
# ======================================================

class SubscribeRequest(BaseModel):
    email: EmailStr

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v):
        return v.lower().strip()


class SubscribeResponse(BaseModel):
    success: bool
    message: str
    email: Optional[str] = None


# ======================================================
# Routes
# ======================================================

@app.get("/")
async def root():
    return {"message": "NextHack Email API Running"}


@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "subscribers": get_count(),
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/subscribe", response_model=SubscribeResponse)
async def subscribe(request: SubscribeRequest):

    email = request.email

    if email_exists(email):
        return SubscribeResponse(
            success=True,
            message="You're already subscribed! 🚀",
            email=email
        )

    try:
        add_subscriber(email)
        logger.info(f"New subscriber added: {email}")

        # Send welcome email
        logger.info(f"Sending welcome email to {email}")
        email_sent = send_welcome_email(email)

        if email_sent:
            mark_email_sent(email)
            logger.info(f"Welcome email sent successfully to {email}")

            return SubscribeResponse(
                success=True,
                message="🎉 Success! Check your inbox or spam for your welcome email.",
                email=email
            )
        else:
            logger.warning(f"Failed to send welcome email to {email}")

            return SubscribeResponse(
                success=True,
                message="🎉 Subscribed! (Welcome email could not be sent)",
                email=email
            )

    except sqlite3.IntegrityError:
        return SubscribeResponse(
            success=True,
            message="You're already subscribed!",
            email=email
        )

    except Exception as e:
        logger.exception("Subscription error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.get("/api/subscribers/count")
async def subscriber_count():
    return {"count": get_count()}


@app.get("/api/subscribers")
async def list_subscribers(limit: int = 100, offset: int = 0):
    """
    Return the full subscriber list (paged) plus total count.
    """
    subscribers = get_all_subscribers(limit=limit, offset=offset)
    total = get_count()
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "subscribers": subscribers,
    }


# ======================================================
# Run Server
# ======================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
