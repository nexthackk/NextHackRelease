# URGENT FIX: Gmail Authentication Error

## The Problem

```
ERROR: SMTP Authentication failed: (535, b'5.7.8 Username and Password not accepted')
```

Your Gmail App Password is **incorrect or invalid** for `alastaair66@gmail.com`.

## Quick Fix Steps

### Step 1: Generate New App Password

1. **Go to Google Account Settings:**
   https://myaccount.google.com/apppasswords

2. **Make sure 2-Factor Authentication is enabled:**
   - If not enabled, go to: https://myaccount.google.com/security
   - Enable 2-Step Verification first
   - Then go back to App Passwords

3. **Generate New App Password:**
   - Select "Mail" as the app
   - Select "Other (Custom name)" as device
   - Enter name: "NextHack"
   - Click "Generate"
   - **Copy the 16-character password** (it looks like: `abcd efgh ijkl mnop`)
   - **Remove all spaces** - it should be 16 characters with no spaces

### Step 2: Update .env File

```bash
cd Website1/backend
nano .env  # or use your preferred editor
```

Update these lines:
```
SMTP_USER=alastaair66@gmail.com
SMTP_PASSWORD=your-16-char-app-password-here  # NO SPACES!
SMTP_FROM_EMAIL=alastaair66@gmail.com  # Make it match SMTP_USER
SMTP_FROM_NAME=NextHack Team
EMAIL_PROVIDER=smtp
```

**Important:**
- Remove ALL spaces from the App Password
- Make sure `SMTP_FROM_EMAIL` matches `SMTP_USER`
- Save the file

### Step 3: Restart Backend Server

**Stop the current backend server** (Ctrl+C), then restart:

```bash
cd Website1/backend
python email_handler.py
```

### Step 4: Test

```bash
# In another terminal
cd Website1/backend
python debug_email.py
```

Enter your email address. If it works, you'll see:
```
✓ SUCCESS: Email sent successfully!
```

## Common Mistakes

❌ **Using regular Gmail password** - Must use App Password
❌ **Spaces in App Password** - Remove all spaces
❌ **Wrong account** - App Password must be for `alastaair66@gmail.com`
❌ **2FA not enabled** - Must enable 2-Step Verification first
❌ **Old/revoked password** - Generate a fresh one

## Verification

After updating `.env` and restarting backend, test with:

```bash
python debug_email.py
```

You should see:
```
[EMAIL SERVICE] Login successful! Sending email...
[EMAIL SERVICE] ✓ Welcome email sent successfully
```

If you still see authentication errors, the App Password is still wrong.

## Alternative: Use Different Gmail Account

If `alastaair66@gmail.com` keeps having issues:

1. Use a different Gmail account
2. Generate App Password for that account
3. Update `.env` with new credentials
4. Restart backend

## Still Not Working?

1. **Double-check App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Make sure you're generating for the correct account
   - Copy the password exactly (no spaces)

2. **Verify 2FA is enabled:**
   - Go to https://myaccount.google.com/security
   - Check "2-Step Verification" is ON

3. **Try regenerating:**
   - Delete old App Password
   - Generate a completely new one
   - Update `.env` file
   - Restart backend

4. **Check .env file location:**
   ```bash
   cd Website1/backend
   ls -la .env
   ```
   Make sure it's in the `backend/` directory!

The error message is clear - Gmail is rejecting your credentials. You need a valid App Password for `alastaair66@gmail.com`.









