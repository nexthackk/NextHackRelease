# Troubleshooting: Welcome Emails Not Received

## Quick Diagnosis

### Step 1: Check if Backend is Running
```bash
cd Website1/backend
python verify_subscription.py
```

If backend is not running, start it:
```bash
python email_handler.py
```

### Step 2: Test Email Sending Directly
```bash
python debug_email.py
```

Enter your email address and check if email is sent.

### Step 3: Check Backend Logs

When a user clicks "Notify Me", you should see in the backend terminal:

**SUCCESS:**
```
[BACKEND] Attempting to send welcome email to user@example.com
[EMAIL SERVICE] ✓ Email sent to user@example.com
[BACKEND] ✓ Welcome email sent successfully to user@example.com
```

**FAILURE:**
```
[BACKEND] Attempting to send welcome email to user@example.com
[BACKEND] ✗ Failed to send welcome email to user@example.com
```

## Common Issues and Solutions

### Issue 1: Backend Server Not Running

**Symptoms:**
- Frontend shows "Unable to connect" error
- No logs in backend terminal

**Solution:**
```bash
cd Website1/backend
python email_handler.py
```

Keep this terminal open while testing.

### Issue 2: Email Sent But Not Received

**Possible Causes:**

1. **Email in Spam Folder**
   - Check spam/junk folder
   - Mark as "Not Spam" if found
   - Add sender to contacts

2. **Email Delivery Delay**
   - Gmail can take 1-5 minutes to deliver
   - Wait a few minutes and check again

3. **Wrong Email Address**
   - Verify the email address entered
   - Check for typos

4. **Email Provider Blocking**
   - Some email providers block automated emails
   - Try a different email address (Gmail works best)

### Issue 3: Email Sending Fails Silently

**Check Backend Logs:**
Look for error messages like:
- `✗ SMTP Authentication failed`
- `✗ Failed to send email via SMTP`
- `Email service configuration issue`

**Solution:**
1. Verify `.env` file has correct credentials
2. Make sure App Password is correct (16 characters, no spaces)
3. Test with `python debug_email.py`

### Issue 4: Frontend Not Connecting to Backend

**Symptoms:**
- Frontend shows connection error
- Backend logs show no requests

**Solution:**
1. Check backend is running on `http://localhost:8000`
2. Check `script.js` has correct API URL:
   ```javascript
   const API_BASE_URL = 'http://localhost:8000/api';
   ```
3. Check browser console for CORS errors
4. Make sure frontend and backend are on same origin or CORS is configured

### Issue 5: Email Configuration Mismatch

**Current Configuration:**
- `SMTP_USER=contactnexthack@gmail.com`
- `SMTP_FROM_EMAIL=nexthack@gmail.com`

**These don't match!** The code automatically uses `SMTP_USER` as From address, but it's better to fix the `.env` file:

```bash
# Edit .env file:
SMTP_USER=contactnexthack@gmail.com
SMTP_FROM_EMAIL=contactnexthack@gmail.com  # Make them match
```

## Step-by-Step Verification

### 1. Verify Email Service Works
```bash
cd Website1/backend
python debug_email.py
```
Enter your email → Should see "✓ SUCCESS: Email sent successfully!"

### 2. Verify Backend API Works
```bash
python verify_subscription.py
```
Enter your email → Should see subscription success message

### 3. Verify Full Flow
1. Start backend: `python email_handler.py`
2. Open `index.html` in browser
3. Enter email and click "Notify Me"
4. Watch backend terminal for logs
5. Check email inbox (and spam folder)

## Debugging Checklist

- [ ] Backend server is running (`python email_handler.py`)
- [ ] `.env` file exists and has correct credentials
- [ ] `SMTP_USER` and `SMTP_PASSWORD` are set correctly
- [ ] App Password is valid (16 characters, generated for correct account)
- [ ] Email test works (`python debug_email.py`)
- [ ] Backend logs show email sending attempts
- [ ] Checked spam folder
- [ ] Verified email address is correct
- [ ] Frontend can connect to backend (check browser console)

## Getting Help

If emails still don't work:

1. **Run diagnostic:**
   ```bash
   python check_setup.py
   ```

2. **Test email directly:**
   ```bash
   python debug_email.py
   ```

3. **Check backend logs** when clicking "Notify Me"

4. **Share the following information:**
   - Output from `check_setup.py`
   - Backend logs when clicking "Notify Me"
   - Any error messages from browser console
   - Whether `debug_email.py` works

## Expected Behavior

When everything works correctly:

1. User clicks "Notify Me"
2. Frontend sends POST to `/api/subscribe`
3. Backend saves email to database
4. Backend immediately sends welcome email
5. Backend logs show: `✓ Welcome email sent successfully`
6. User receives email within 1-5 minutes
7. Email appears in inbox (or spam folder)

If any step fails, check the logs to see where it stops.









