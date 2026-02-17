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
# Environment Variables
# =====================================================

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "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")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", "<contactnexthack@gmail.com>")
SENDGRID_FROM_NAME = os.getenv("SENDGRID_FROM_NAME", "NextHack Team")


# =====================================================
# Welcome Email Template
# =====================================================

def get_welcome_email_template() -> Dict[str, str]:

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to NextHack</title>
    </head>
    <body style="margin:0; padding:0; font-family:'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; background-color:#0A0A0F; color:#FFFFFF;">
        <table role="presentation" style="width:100%; border-collapse:collapse; background-color:#0A0A0F;">
            <tr>
                <td align="center" style="padding:40px 20px;">
                    <table role="presentation" style="max-width:600px; width:100%; border-collapse:collapse; background:linear-gradient(135deg,#111118 0%,#1a1a24 100%); border-radius:20px; overflow:hidden; box-shadow:0 8px 32px rgba(0,0,0,0.3);">

                        <!-- Header -->
                        <tr>
                            <td style="background:linear-gradient(135deg,#6366F1 0%,#8B5CF6 50%,#EC4899 100%); padding:40px 30px; text-align:center;">
                                <h1 style="margin:0; font-size:32px; font-weight:800; color:#FFFFFF;">
                                    🚀 Welcome to NextHack!
                                </h1>
                            </td>
                        </tr>

                        <!-- Content -->
                        <tr>
                            <td style="padding:40px 30px;">

                                <p style="font-size:18px; line-height:1.6; color:#FFFFFF;">
                                    Hi there!
                                </p>

                                <p style="font-size:16px; line-height:1.8; color:#A1A1AA;">
                                    Thank you for joining the NextHack community! We're thrilled to have you on board.
                                </p>

                                <p style="font-size:16px; line-height:1.8; color:#A1A1AA;">
                                    You've taken the first step towards revolutionizing your cybersecurity approach.
                                    NextHack is being built with cutting-edge AI technology to provide you with:
                                </p>

                                <ul style="color:#A1A1AA; font-size:16px; line-height:1.8; padding-left:20px;">
                                    <li>🤖 <strong style="color:#FFFFFF;">AI-Powered Vulnerability Scanning</strong> - Detect threats with unprecedented accuracy</li>
                                    <li>⚡ <strong style="color:#FFFFFF;">Real-Time Threat Detection</strong> - Stay protected 24/7</li>
                                    <li>📊 <strong style="color:#FFFFFF;">Comprehensive Security Reports</strong> - Get actionable insights</li>
                                    <li>🛡️ <strong style="color:#FFFFFF;">Advanced Security Frameworks</strong> - OWASP, MITRE ATT&CK, NIST compliance</li>
                                </ul>

                                <p style="font-size:16px; line-height:1.8; color:#A1A1AA;">
                                    We're working hard to bring you the most advanced security platform.
                                    As an early subscriber, you'll be among the first to know when we launch
                                    and will receive exclusive updates about our progress.
                                </p>

                                <blockquote style="margin:30px 0; padding:20px; background-color:#111118; border-left:4px solid #6366F1; color:#FFFFFF; font-style:italic;">
                                    "Security is not a product, but a process. We're here to make that process smarter, faster, and more effective."
                                </blockquote>

                                <p style="font-size:16px; line-height:1.8; color:#A1A1AA;">
                                    Stay tuned for exciting updates! We can't wait to show you what we've been building.
                                </p>

                                <p style="margin-top:30px; font-size:16px; color:#A1A1AA;">
                                    Best regards,<br>
                                    <strong style="color:#FFFFFF;">The NextHack Team</strong>
                                </p>

                            </td>
                        </tr>

                        <!-- Footer -->
                        <tr>
                            <td style="padding:20px; background-color:#0A0A0F; text-align:center;">
                                <p style="font-size:12px; color:#71717A;">
                                    You're receiving this email because you subscribed to NextHack launch notifications.
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

    text_content = """
Welcome to NextHack!

Hi there!

Thank you for joining the NextHack community! We're thrilled to have you on board.

You've taken the first step towards revolutionizing your cybersecurity approach.
NextHack is being built with cutting-edge AI technology to provide you with:

🤖 AI-Powered Vulnerability Scanning - Detect threats with unprecedented accuracy
⚡ Real-Time Threat Detection - Stay protected 24/7
📊 Comprehensive Security Reports - Get actionable insights
🛡️ Advanced Security Frameworks - OWASP, MITRE ATT&CK, NIST compliance

We're working hard to bring you the most advanced security platform.
As an early subscriber, you'll be among the first to know when we launch
and will receive exclusive updates about our progress.

"Security is not a product, but a process. We're here to make that process smarter, faster, and more effective."

Stay tuned for exciting updates! We can't wait to show you what we've been building.

Best regards,
The NextHack Team
"""

    return {
        "subject": "🚀 Welcome to NextHack – You're On Board!",
        "html": html_content,
        "text": text_content,
    }


# =====================================================
# Send Email via SendGrid
# =====================================================

def send_welcome_email(to_email: str) -> bool:
    try:
        if not SENDGRID_API_KEY:
            logger.error("SENDGRID_API_KEY not configured")
            return False

        if not SENDGRID_FROM_EMAIL:
            logger.error("SENDGRID_FROM_EMAIL not configured")
            return False

        email_content = get_welcome_email_template()

        sg = SendGridAPIClient(SENDGRID_API_KEY)

        message = Mail(
            from_email=SENDGRID_FROM_NAME,
            to_emails=to_email,
            subject=email_content["subject"],
            plain_text_content=email_content["text"],
            html_content=email_content["html"],
        )

        response = sg.send(message)

        logger.info(f"SendGrid response status: {response.status_code}")

        return response.status_code == 202

    except Exception as e:
        logger.exception(f"Failed to send welcome email: {e}")
        return False
