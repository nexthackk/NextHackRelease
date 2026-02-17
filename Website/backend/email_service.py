"""
Email Service for Sending Welcome Emails
Supports SMTP, SendGrid, and Mailgun
"""

import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict
from pathlib import Path

# Initialize logger first
logger = logging.getLogger(__name__)

# Try to load environment variables from .env file FIRST
try:
    from dotenv import load_dotenv
    # Load .env file from the same directory as this file
    env_path = Path(__file__).parent / '.env'
    # Use override=True to ensure new values replace old ones
    load_dotenv(dotenv_path=env_path, override=True)
    logger.info(f"Email service loaded .env from: {env_path}")
except ImportError:
    pass  # python-dotenv not installed, use system env vars
except Exception as e:
    logger.error(f"Error loading .env in email_service: {e}")

def get_smtp_config():
    """Get SMTP configuration dynamically from environment (always fresh)"""
    # Reload .env to ensure we have latest values
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent / '.env'
        load_dotenv(dotenv_path=env_path, override=True)
    except:
        pass
    
    return {
        "EMAIL_PROVIDER": os.getenv("EMAIL_PROVIDER", "smtp").lower(),
        "SMTP_HOST": os.getenv("SMTP_HOST", "smtp.gmail.com"),
        "SMTP_PORT": int(os.getenv("SMTP_PORT", "587")),
        "SMTP_USER": os.getenv("SMTP_USER", ""),
        "SMTP_PASSWORD": os.getenv("SMTP_PASSWORD", ""),
        "SMTP_FROM_EMAIL": os.getenv("SMTP_FROM_EMAIL", os.getenv("SMTP_USER", "")),
        "SMTP_FROM_NAME": os.getenv("SMTP_FROM_NAME", "NextHack Team"),
    }

# Email configuration from environment variables (for backward compatibility)
# These are loaded at import time, but get_smtp_config() should be used for fresh values
EMAIL_PROVIDER = get_smtp_config()["EMAIL_PROVIDER"]
SMTP_HOST = get_smtp_config()["SMTP_HOST"]
SMTP_PORT = get_smtp_config()["SMTP_PORT"]
SMTP_USER = get_smtp_config()["SMTP_USER"]
SMTP_PASSWORD = get_smtp_config()["SMTP_PASSWORD"]
SMTP_FROM_EMAIL = get_smtp_config()["SMTP_FROM_EMAIL"]
SMTP_FROM_NAME = get_smtp_config()["SMTP_FROM_NAME"]

# SendGrid Configuration
# SendGrid Configuration
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "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")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", "contactnexthack@gmail.com")
SENDGRID_FROM_NAME = os.getenv("SENDGRID_FROM_NAME", "NextHack Team")



# Mailgun Configuration
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY", "")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN", "")


def get_welcome_email_template(email: str) -> Dict[str, str]:
    """
    Generate welcome email HTML and text content
    """
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to NextHack!</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; background-color: #0A0A0F; color: #FFFFFF;">
        <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #0A0A0F;">
            <tr>
                <td align="center" style="padding: 40px 20px;">
                    <table role="presentation" style="max-width: 600px; width: 100%; border-collapse: collapse; background: linear-gradient(135deg, #111118 0%, #1a1a24 100%); border-radius: 20px; overflow: hidden; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);">
                        <!-- Header with gradient -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #EC4899 100%); padding: 40px 30px; text-align: center;">
                                <h1 style="margin: 0; font-size: 32px; font-weight: 800; color: #FFFFFF; font-family: 'Space Grotesk', sans-serif;">
                                    🚀 Welcome to NextHack!
                                </h1>
                            </td>
                        </tr>
                        
                        <!-- Main Content -->
                        <tr>
                            <td style="padding: 40px 30px;">
                                <p style="margin: 0 0 20px 0; font-size: 18px; line-height: 1.6; color: #FFFFFF;">
                                    Hi there!
                                </p>
                                
                                <p style="margin: 0 0 20px 0; font-size: 16px; line-height: 1.8; color: #A1A1AA;">
                                    Thank you for joining the NextHack community! We're thrilled to have you on board.
                                </p>
                                
                                <p style="margin: 0 0 20px 0; font-size: 16px; line-height: 1.8; color: #A1A1AA;">
                                    You've taken the first step towards revolutionizing your cybersecurity approach. NextHack is being built with cutting-edge AI technology to provide you with:
                                </p>
                                
                                <ul style="margin: 20px 0; padding-left: 20px; color: #A1A1AA; font-size: 16px; line-height: 1.8;">
                                    <li style="margin-bottom: 10px;">🤖 <strong style="color: #FFFFFF;">AI-Powered Vulnerability Scanning</strong> - Detect threats with unprecedented accuracy</li>
                                    <li style="margin-bottom: 10px;">⚡ <strong style="color: #FFFFFF;">Real-Time Threat Detection</strong> - Stay protected 24/7</li>
                                    <li style="margin-bottom: 10px;">📊 <strong style="color: #FFFFFF;">Comprehensive Security Reports</strong> - Get actionable insights</li>
                                    <li style="margin-bottom: 10px;">🛡️ <strong style="color: #FFFFFF;">Advanced Security Frameworks</strong> - OWASP, MITRE ATT&CK, NIST compliance</li>
                                </ul>
                                
                                <p style="margin: 20px 0; font-size: 16px; line-height: 1.8; color: #A1A1AA;">
                                    We're working hard to bring you the most advanced security platform. As an early subscriber, you'll be among the first to know when we launch and will receive exclusive updates about our progress.
                                </p>
                                
                                <div style="margin: 30px 0; padding: 20px; background: rgba(99, 102, 241, 0.1); border-left: 4px solid #6366F1; border-radius: 8px;">
                                    <p style="margin: 0; font-size: 15px; line-height: 1.6; color: #818CF8; font-style: italic;">
                                        "Security is not a product, but a process. We're here to make that process smarter, faster, and more effective."
                                    </p>
                                </div>
                                
                                <p style="margin: 20px 0 0 0; font-size: 16px; line-height: 1.8; color: #A1A1AA;">
                                    Stay tuned for exciting updates! We can't wait to show you what we've been building.
                                </p>
                                
                                <p style="margin: 30px 0 0 0; font-size: 16px; line-height: 1.8; color: #A1A1AA;">
                                    Best regards,<br>
                                    <strong style="color: #FFFFFF;">The NextHack Team</strong>
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="padding: 30px; background-color: #0A0A0F; text-align: center; border-top: 1px solid rgba(255, 255, 255, 0.1);">
                                <p style="margin: 0 0 15px 0; font-size: 14px; color: #71717A;">
                                    You're receiving this email because you subscribed to NextHack launch notifications.
                                </p>
                                <p style="margin: 0; font-size: 12px; color: #71717A;">
                                    &copy; 2025 NextHack. All rights reserved.
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    text_content = f"""
    Welcome to NextHack!

    Hi there!

    Thank you for joining the NextHack Launch! We're thrilled to have you on board.

    You've taken the first step towards revolutionizing your cybersecurity approach. NextHack is being built with cutting-edge AI technology to provide you with:

    - AI-Powered Vulnerability Scanning - Detect threats with unprecedented accuracy
    - Real-Time Threat Detection - Stay protected 24/7
    - Comprehensive Security Reports - Get actionable insights
    - Advanced Security Frameworks - OWASP, MITRE ATT&CK, NIST compliance

    We're working hard to bring you the most advanced security platform. As an early subscriber, you'll be among the first to know when we launch and will receive exclusive updates about our progress.

    "Security is not a product, but a process. We're here to make that process smarter, faster, and more effective."

    Stay tuned for exciting updates! We can't wait to show you what we've been building.

    Best regards,
    The NextHack Team

    ---
    You're receiving this email because you subscribed to NextHack launch notifications.
    © 2026 NextHack. All rights reserved.
    """
    
    return {
        "html": html_content,
        "text": text_content,
        "subject": "NextHack - You're On Board!"
    }


def send_email_sendgrid(to_email: str, subject: str, html_content: str, text_content: str) -> bool:
    """Send email using SendGrid API"""
    try:
        if not SENDGRID_API_KEY:
            logger.error("SENDGRID_API_KEY not configured.")
            print("[EMAIL SERVICE] ✗ SENDGRID_API_KEY not configured")
            return False

        if not SENDGRID_FROM_EMAIL:
            logger.error("SENDGRID_FROM_EMAIL not configured.")
            print("[EMAIL SERVICE] ✗ SENDGRID_FROM_EMAIL not configured")
            return False

        import sendgrid
        from sendgrid.helpers.mail import Mail

        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

        message = Mail(
            from_email=f"{SENDGRID_FROM_NAME} <{SENDGRID_FROM_EMAIL}>",
            to_emails=to_email,
            subject=subject,
            plain_text_content=text_content,
            html_content=html_content
        )

        response = sg.send(message)

        print(f"[EMAIL SERVICE] SendGrid status: {response.status_code}")

        if response.status_code in [200, 201, 202]:
            logger.info(f"✓ Welcome email sent to {to_email} via SendGrid")
            print(f"[EMAIL SERVICE] ✓ Email sent successfully")
            return True
        else:
            logger.error(f"SendGrid failed: {response.status_code} - {response.body}")
            print(f"[EMAIL SERVICE] ✗ SendGrid failed")
            return False

    except Exception as e:
        logger.error(f"SendGrid Exception: {e}", exc_info=True)
        print(f"[EMAIL SERVICE] ✗ SendGrid exception: {e}")
        return False


def send_email_mailgun(to_email: str, subject: str, html_content: str, text_content: str) -> bool:
    """Send email using Mailgun API"""
    try:
        if not MAILGUN_API_KEY or not MAILGUN_DOMAIN:
            logger.warning("Mailgun credentials not configured. Email not sent.")
            return False
        
        import requests
        
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f"{SMTP_FROM_NAME} <mailgun@{MAILGUN_DOMAIN}>",
                "to": to_email,
                "subject": subject,
                "text": text_content,
                "html": html_content
            }
        )
        
        if response.status_code == 200:
            logger.info(f"Welcome email sent successfully to {to_email} via Mailgun")
            return True
        else:
            logger.error(f"Mailgun API error: {response.status_code} - {response.text}")
            return False
            
    except ImportError:
        logger.error("Requests library not installed. Install with: pip install requests")
        return False
    except Exception as e:
        logger.error(f"Failed to send email via Mailgun: {e}")
        return False


def send_welcome_email(to_email: str) -> bool:
    """
    Send welcome email to a new subscriber
    Returns True if email was sent successfully, False otherwise
    """
    try:
        email_content = get_welcome_email_template(to_email)
        
        provider = get_smtp_config()["EMAIL_PROVIDER"]
        
        if EMAIL_PROVIDER == "sendgrid":
            return send_email_sendgrid(
                to_email,
                email_content["subject"],
                email_content["html"],
                email_content["text"]
            )
        elif EMAIL_PROVIDER == "mailgun":
            return send_email_mailgun(
                to_email,
                email_content["subject"],
                email_content["html"],
                email_content["text"]
            )
        else:  # Default to SMTP
            return send_email_smtp(
                to_email,
                email_content["subject"],
                email_content["html"],
                email_content["text"]
            )
            
    except Exception as e:
        logger.error(f"Error sending welcome email to {to_email}: {e}")
        return False

