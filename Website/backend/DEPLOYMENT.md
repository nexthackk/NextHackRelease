# Deployment Guide for Website1 Backend

## Fixed Issues
✅ Updated `requirements.txt` with versions that have pre-built wheels (no Rust compilation needed)
✅ Added `runtime.txt` to pin Python 3.12.8 for better compatibility
✅ Updated Pydantic validator syntax from v1 to v2 (`@validator` → `@field_validator`)
✅ Updated CORS to read from environment variables

## Render Deployment Steps

### 1. Push Changes to GitHub
```bash
cd "/Users/pratik/Desktop/NewTest copy"
git add Website1/backend/requirements.txt Website1/backend/runtime.txt Website1/backend/email_handler.py
git commit -m "Fix deployment: update dependencies and Pydantic v2 syntax"
git push origin main
```

### 2. Render Web Service Settings

**Basic Settings:**
- **Name**: `nexthack-api` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main`

**Build & Deploy:**
- **Root Directory**: Leave empty (or set to `Website1` if your repo structure requires it)
- **Build Command**: 
  ```bash
  pip install -r Website1/backend/requirements.txt
  ```
  OR if root directory is set to `Website1`:
  ```bash
  pip install -r backend/requirements.txt
  ```
- **Start Command**: 
  ```bash
  cd Website1/backend && uvicorn email_handler:app --host 0.0.0.0 --port $PORT
  ```
  OR if root directory is set to `Website1`:
  ```bash
  uvicorn backend.email_handler:app --host 0.0.0.0 --port $PORT
  ```

**Important**: Render uses `$PORT` environment variable automatically. Use `$PORT` instead of hardcoding `8000`.

### 3. Environment Variables in Render

Add all variables from your `Website1/backend/.env` file:

**Required:**
- `SMTP_HOST` - Your SMTP server (e.g., `smtp.gmail.com`)
- `SMTP_PORT` - SMTP port (e.g., `587` for TLS)
- `SMTP_USER` - Your email address
- `SMTP_PASSWORD` - Your email password or app password
- `FROM_EMAIL` - Sender email address
- `FROM_NAME` - Sender name (e.g., "NextHack Team")

**Optional:**
- `ALLOWED_ORIGINS` - Comma-separated list of frontend URLs (e.g., `https://nexthack-landing.netlify.app`)
  - If not set, defaults to `*` (allows all origins)
  - **Recommended for production**: Set your Netlify URL here

**Example:**
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com
FROM_NAME=NextHack Team
ALLOWED_ORIGINS=https://nexthack-landing.netlify.app
```

### 4. After Deployment

1. **Get your Render URL**: Something like `https://nexthack-api.onrender.com`
2. **Test the API**: Visit `https://nexthack-api.onrender.com/docs` to see the FastAPI docs
3. **Update frontend**: Update `Website1/script.js`:
   ```js
   const API_BASE_URL = 'https://nexthack-api.onrender.com/api';
   ```

## Troubleshooting

### Build fails with Rust/pydantic-core error
- ✅ Fixed by updating to pydantic 2.10.0+ which has pre-built wheels
- Make sure `runtime.txt` specifies Python 3.12.8

### CORS errors in browser console
- Check that `ALLOWED_ORIGINS` in Render includes your Netlify URL
- Or temporarily set to `*` for testing (not recommended for production)

### Email not sending
- Verify all SMTP environment variables are set correctly in Render
- Check Render logs for SMTP connection errors
- Test SMTP credentials locally first

### Port binding error
- Make sure start command uses `$PORT` not hardcoded `8000`
- Render automatically sets `$PORT` environment variable
