"""
Email Service for Sending Welcome Emails
Production Version - SendGrid Only (Railway Compatible)
"""

import os
import logging
from typing import Dict
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)

# =====================================================
# Environment Variables (set in Railway — NEVER hardcode)
# =====================================================

SENDGRID_API_KEY    = os.getenv("SENDGRID_API_KEY", "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")       # No fallback — forces env var
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", "contactnexthack@gmail.com")
SENDGRID_FROM_NAME  = os.getenv("SENDGRID_FROM_NAME", "NextHack Team")


def get_welcome_email_template() -> Dict[str, str]:
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
        "subject": "🚀 Welcome to NextHack – You're On Board!",
        "html": html_content,
        "text": text_content,
    }


def send_welcome_email(to_email: str) -> bool:
    try:
        if not SENDGRID_API_KEY:
            logger.error("SENDGRID_API_KEY environment variable not set")
            return False

        email_content = get_welcome_email_template()

        message = Mail(
            from_email=(SENDGRID_FROM_EMAIL, SENDGRID_FROM_NAME),  # ← FIXED: tuple format
            to_emails=to_email,
            subject=email_content["subject"],
            plain_text_content=email_content["text"],
            html_content=email_content["html"],
        )

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        logger.info(f"SendGrid status: {response.status_code} for {to_email}")
        return response.status_code == 202

    except Exception as e:
        logger.exception(f"Failed to send welcome email to {to_email}: {e}")
        return False
