# Quick Fix: Welcome Emails Not Sending

## Immediate Steps

### 1. Make Sure Backend is Running
```bash
cd Website1/backend
python email_handler.py
```
**Keep this terminal open!** You need to see the logs.

### 2. Test Email Sending
In a NEW terminal:
```bash
cd Website1/backend
python debug_email.py
```
Enter your email address. If this works, email service is fine.

### 3. Test Full Subscription
```bash
python verify_subscription.py
```
Enter your email. This tests the full API flow.

### 4. Check Backend Logs

When you click "Notify Me" on the website, you should see in the backend terminal:

```
[BACKEND] Attempting to send welcome email to user@example.com
[EMAIL SERVICE] ✓ Email sent to user@example.com
[BACKEND] ✓ Welcome email sent successfully to user@example.com
```

**If you see errors instead, that's the problem!**

## Most Common Issues

### ❌ "Backend not running"
**Fix:** Start backend with `python email_handler.py`

### ❌ "SMTP Authentication failed"
**Fix:** 
1. Check `.env` file has correct App Password
2. Make sure App Password is for `contactnexthack@gmail.com`
3. Regenerate App Password: https://myaccount.google.com/apppasswords

### ❌ "Email sent but not received"
**Fix:**
1. Check spam folder
2. Wait 1-5 minutes (Gmail delivery delay)
3. Try different email address

### ❌ "No logs in backend"
**Fix:**
1. Frontend might not be connecting to backend
2. Check browser console for errors
3. Verify API URL in `script.js` is `http://localhost:8000/api`

## What to Check Right Now

1. **Is backend running?**
   ```bash
   curl http://localhost:8000/api/health
   ```
   Should return JSON with "status": "healthy"

2. **Does email test work?**
   ```bash
   python debug_email.py
   ```
   Should show "✓ SUCCESS"

3. **What do backend logs show?**
   When clicking "Notify Me", check the backend terminal for messages.

## Still Not Working?

Run full diagnostic:
```bash
python check_setup.py
```

Then share:
- Output from `check_setup.py`
- Backend logs when clicking "Notify Me"
- Output from `debug_email.py`









