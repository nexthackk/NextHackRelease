# Email Configuration Guide

This guide will help you set up email sending for the NextHack landing page.

## Quick Setup Options

### Option 1: Gmail SMTP (Easiest for Testing)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Enter "NextHack" as the name
   - Copy the generated 16-character password

3. **Set Environment Variables**:
   ```bash
   export SMTP_USER=your-email@gmail.com
   export SMTP_PASSWORD=your-16-char-app-password
   export SMTP_FROM_EMAIL=your-email@gmail.com
   export SMTP_FROM_NAME="NextHack Team"
   ```

4. **Or create a `.env` file** in the `backend` directory:
   ```
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-16-char-app-password
   SMTP_FROM_EMAIL=your-email@gmail.com
   SMTP_FROM_NAME=NextHack Team
   EMAIL_PROVIDER=smtp
   ```

### Option 2: SendGrid (Recommended for Production)

1. **Sign up** at https://sendgrid.com (free tier: 100 emails/day)
2. **Create an API Key**:
   - Go to Settings > API Keys
   - Create a new API key with "Mail Send" permissions
   - Copy the API key

3. **Set Environment Variables**:
   ```bash
   export SENDGRID_API_KEY=your-api-key
   export EMAIL_PROVIDER=sendgrid
   export SMTP_FROM_EMAIL=your-verified-sender@yourdomain.com
   export SMTP_FROM_NAME=NextHack Team
   ```

### Option 3: Mailgun (Alternative)

1. **Sign up** at https://www.mailgun.com (free tier: 5,000 emails/month)
2. **Get your API key and domain** from the dashboard
3. **Set Environment Variables**:
   ```bash
   export MAILGUN_API_KEY=your-api-key
   export MAILGUN_DOMAIN=your-domain.mailgun.org
   export EMAIL_PROVIDER=mailgun
   export SMTP_FROM_EMAIL=noreply@yourdomain.com
   export SMTP_FROM_NAME=NextHack Team
   ```

## Using Environment Variables

### Method 1: Export in Terminal
```bash
export SMTP_USER=your-email@gmail.com
export SMTP_PASSWORD=your-password
python email_handler.py
```

### Method 2: Create .env File
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your credentials

3. Install python-dotenv:
   ```bash
   pip install python-dotenv
   ```

4. Update `email_handler.py` to load .env:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

### Method 3: System Environment Variables
Set them in your system's environment (varies by OS).

## Testing Email Sending

1. **Start the backend server**:
   ```bash
   cd backend
   python email_handler.py
   ```

2. **Subscribe with a test email** via the frontend or API

3. **Check the logs** for email sending status

4. **Check the recipient's inbox** (and spam folder)

## Troubleshooting

### Gmail SMTP Issues
- Make sure you're using an **App Password**, not your regular password
- Enable "Less secure app access" if using older Gmail accounts (not recommended)
- Check that 2FA is enabled

### SendGrid Issues
- Verify your sender email address in SendGrid dashboard
- Check API key permissions
- Review SendGrid activity logs

### Mailgun Issues
- Verify your domain in Mailgun dashboard
- Check API key is correct
- Review Mailgun logs

### General Issues
- Check firewall/network settings
- Verify all environment variables are set correctly
- Check server logs for detailed error messages

## Email Template Customization

Edit `email_service.py` and modify the `get_welcome_email_template()` function to customize:
- Email subject
- HTML content
- Text content
- Branding and colors

## Production Recommendations

1. **Use a dedicated email service** (SendGrid, Mailgun, AWS SES) instead of personal Gmail
2. **Set up SPF, DKIM, and DMARC** records for your domain
3. **Monitor email delivery rates** and bounce rates
4. **Implement rate limiting** to prevent abuse
5. **Add email verification** (optional but recommended)
6. **Set up email analytics** to track opens and clicks

## Security Notes

- **Never commit** `.env` files or credentials to version control
- **Use environment variables** or secure secret management
- **Rotate API keys** regularly
- **Monitor** for unauthorized access









