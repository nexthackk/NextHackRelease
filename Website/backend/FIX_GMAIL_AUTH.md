# Fix Gmail Authentication Error

## Error Message
```
535, b'5.7.8 Username and Password not accepted
```

## Problem Identified

Your `.env` file has:
- `SMTP_USER=contactnexthack@gmail.com`
- `SMTP_FROM_EMAIL=nexthack@gmail.com`

**These are different email addresses!** Gmail requires that:
1. You authenticate with the account that has the app password
2. The "From" email must match the authenticated account (or be an alias)

## Solutions

### Solution 1: Use Same Email for Both (Recommended)

**Option A: Use contactnexthack@gmail.com for both**
```bash
# Edit .env file:
SMTP_USER=contactnexthack@gmail.com
SMTP_PASSWORD=your-app-password-for-contactnexthack
SMTP_FROM_EMAIL=contactnexthack@gmail.com
SMTP_FROM_NAME=NextHack Team
```

**Option B: Use nexthack@gmail.com for both**
```bash
# Edit .env file:
SMTP_USER=nexthack@gmail.com
SMTP_PASSWORD=your-app-password-for-nexthack
SMTP_FROM_EMAIL=nexthack@gmail.com
SMTP_FROM_NAME=NextHack Team
```

### Solution 2: Generate Correct App Password

1. **Go to Google Account**: https://myaccount.google.com/
2. **Enable 2-Factor Authentication** (if not already enabled)
3. **Generate App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Enter "NextHack" as the name
   - Copy the 16-character password (no spaces)
4. **Update .env file**:
   ```bash
   SMTP_USER=contactnexthack@gmail.com  # The account you generated app password for
   SMTP_PASSWORD=xxxx xxxx xxxx xxxx    # The 16-character app password (remove spaces)
   SMTP_FROM_EMAIL=contactnexthack@gmail.com  # Must match SMTP_USER
   ```

### Solution 3: Use Gmail Alias (Advanced)

If you want to send from `nexthack@gmail.com` but authenticate with `contactnexthack@gmail.com`:

1. **Set up email alias** in Gmail settings
2. **Or use SMTP relay** with proper authentication
3. **Or use a service like SendGrid/Mailgun** (recommended for production)

## Quick Fix Steps

1. **Decide which email to use** (contactnexthack@gmail.com or nexthack@gmail.com)

2. **Generate App Password for that account**:
   ```
   https://myaccount.google.com/apppasswords
   ```

3. **Update .env file**:
   ```bash
   cd Website1/backend
   nano .env  # or use your preferred editor
   ```
   
   Make sure both SMTP_USER and SMTP_FROM_EMAIL are the same:
   ```
   SMTP_USER=contactnexthack@gmail.com
   SMTP_PASSWORD=your-16-char-app-password
   SMTP_FROM_EMAIL=contactnexthack@gmail.com
   SMTP_FROM_NAME=NextHack Team
   EMAIL_PROVIDER=smtp
   ```

4. **Test the fix**:
   ```bash
   python test_email.py
   ```

## Common Issues

### Issue: "App Password not working"
- Make sure 2FA is enabled
- Regenerate the app password
- Remove spaces from the app password
- Make sure you're using the correct account

### Issue: "Still getting authentication error"
- Verify SMTP_USER matches the account that generated the app password
- Make sure SMTP_FROM_EMAIL matches SMTP_USER
- Check that the app password is correct (16 characters, no spaces)
- Try regenerating the app password

### Issue: "Want to send from different email"
- Use Gmail aliases (if both accounts are yours)
- Or use a professional email service (SendGrid, Mailgun, AWS SES)
- Or set up SMTP relay with proper authentication

## Verification

After fixing, test with:
```bash
cd Website1/backend
python test_email.py
```

Enter your email address and check if the welcome email arrives.

## Code Update

I've updated the code to automatically use `SMTP_USER` as the From email if they don't match. However, **it's still recommended to make them match** in your `.env` file to avoid confusion.









