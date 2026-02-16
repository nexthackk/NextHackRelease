#!/bin/bash

# SecTool Coming Soon Landing Page - Startup Script

echo "🚀 Starting SecTool Coming Soon Landing Page..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if backend dependencies are installed
if [ ! -d "backend" ]; then
    echo "❌ Backend directory not found!"
    exit 1
fi

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Start the backend server
echo ""
echo "✅ Starting backend API server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "💡 To view the frontend, open index.html in your browser"
echo "   Or run: python3 -m http.server 3000 (in the Website1 directory)"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python email_handler.py









