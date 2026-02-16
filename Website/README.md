# SecTool - Coming Soon Landing Page

A beautiful, modern landing page for collecting email addresses from users interested in the SecTool product launch.

## Features

✨ **Modern Design**
- Beautiful gradient animations
- Smooth transitions and hover effects
- Fully responsive design
- Dark theme with glassmorphism effects

📧 **Email Collection**
- Real-time email validation
- Backend API for storing subscribers
- **Automatic welcome emails** sent to new subscribers
- Local storage fallback
- Success/error messaging

🎨 **UI/UX Highlights**
- Animated background with gradient orbs
- Smooth scroll animations
- Interactive form with loading states
- Feature cards with hover effects
- Professional typography

## Project Structure

```
Website1/
├── index.html          # Main landing page
├── styles.css          # All styling
├── script.js           # Frontend JavaScript
├── backend/
│   ├── email_handler.py    # FastAPI backend for email collection
│   ├── email_service.py     # Email sending service (SMTP/SendGrid/Mailgun)
│   ├── requirements.txt     # Python dependencies
│   ├── EMAIL_SETUP.md      # Email configuration guide
│   └── .env.example        # Environment variables template
├── subscribers.db      # SQLite database (created automatically)
└── README.md          # This file
```

## Setup Instructions

### Frontend (Static Files)

The frontend is ready to use! Simply open `index.html` in a web browser or serve it with any static file server.

**Option 1: Direct Open**
```bash
# Just open index.html in your browser
open index.html  # macOS
# or double-click the file
```

**Option 2: Python Simple Server**
```bash
cd Website1
python3 -m http.server 3000
# Then visit http://localhost:3000
```

**Option 3: Node.js http-server**
```bash
npx http-server -p 3000
# Then visit http://localhost:3000
```

### Backend (Email Collection API)

1. **Install Python Dependencies**
```bash
cd Website1/backend
pip install -r requirements.txt
```

2. **Configure Email Settings** (Required for welcome emails)

   See `backend/EMAIL_SETUP.md` for detailed instructions. Quick setup:

   **Gmail SMTP** (Easiest for testing):
   ```bash
   export SMTP_USER=your-email@gmail.com
   export SMTP_PASSWORD=your-app-password
   export SMTP_FROM_EMAIL=your-email@gmail.com
   export SMTP_FROM_NAME="NextHack Team"
   ```

   **SendGrid** (Recommended for production):
   ```bash
   export SENDGRID_API_KEY=your-api-key
   export EMAIL_PROVIDER=sendgrid
   ```

   Or create a `.env` file in the `backend` directory (see `.env.example`).

3. **Start the API Server**
```bash
python email_handler.py
```

The API will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

3. **Update Frontend API URL** (if needed)

If you're running the backend on a different port or domain, update the `API_BASE_URL` in `script.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

## Usage

### For Users
1. Visit the landing page
2. Enter your email address
3. Click "Notify Me"
4. You'll receive a confirmation message
5. You'll be notified when the product launches!

### For Developers

#### API Endpoints

**Subscribe**
```bash
POST /api/subscribe
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**Get Subscriber Count**
```bash
GET /api/subscribers/count
```

**List All Subscribers** (Admin)
```bash
GET /api/subscribers?limit=100&offset=0
```

**Export Subscribers** (Admin)
```bash
GET /api/subscribers/export
```

#### Database

Subscribers are stored in a SQLite database (`subscribers.db`) with the following schema:

- `id`: Primary key
- `email`: Email address (unique)
- `subscribed_at`: Timestamp
- `ip_address`: IP address (optional)
- `user_agent`: User agent (optional)
- `verified`: Boolean (for future email verification)
- `notified`: Boolean (to track if launch email was sent)

## Customization

### Colors & Branding

Edit CSS variables in `styles.css`:

```css
:root {
    --primary: #6366F1;        /* Main brand color */
    --secondary: #8B5CF6;      /* Secondary color */
    --accent: #EC4899;         /* Accent color */
    /* ... more variables */
}
```

### Content

Edit text content in `index.html`:
- Hero title and description
- Feature cards
- Footer text
- Social media links

### Features

Add or modify feature cards in the `features-preview` section of `index.html`.

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- Optimized animations with CSS transforms
- Lazy loading for images (if added)
- Minimal JavaScript footprint
- Fast API responses

## Security Notes

- Email validation on both frontend and backend
- SQL injection protection via parameterized queries
- CORS configured (update for production)
- Input sanitization

## Production Deployment

### Frontend
- Deploy `index.html`, `styles.css`, and `script.js` to any static hosting:
  - Netlify
  - Vercel
  - GitHub Pages
  - AWS S3 + CloudFront
  - Any CDN

### Backend
- Deploy the FastAPI backend to:
  - Heroku
  - AWS Lambda
  - Google Cloud Run
  - DigitalOcean App Platform
  - Any Python hosting service

### Production Checklist
- [ ] Update CORS origins to your domain
- [ ] Set up email verification (optional)
- [ ] Configure email sending service (SendGrid, Mailgun, etc.)
- [ ] Set up database backups
- [ ] Add rate limiting
- [ ] Enable HTTPS
- [ ] Add analytics tracking
- [ ] Test on multiple devices

## License

This project is part of the SecTool application.

## Support

For issues or questions, please contact the development team.

---

**Built with ❤️ for SecTool**

