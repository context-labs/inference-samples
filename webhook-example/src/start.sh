#!/bin/bash

echo "🚀 Magnus Detection API Setup"
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "❌ Virtual environment not activated!"
    echo "Please activate it first from the project root:"
    echo "  source .venv/bin/activate"
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please create .env with:"
    echo "  DATABASE_URL=..."
    echo "  INFERENCE_API_KEY=..."
    echo "  INFERENCE_WEBHOOK_ID=..."
    exit 1
fi

# Initialize database
echo "📊 Initializing database..."
python init_db.py

# Start ngrok in background
echo "🌐 Starting ngrok..."
ngrok http 8000 &
NGROK_PID=$!

echo "⏳ Waiting for ngrok to start..."
sleep 3

# Get ngrok URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*' | grep -o 'https://[^"]*' | head -1)

if [ -z "$NGROK_URL" ]; then
    echo "❌ Failed to get ngrok URL"
    kill $NGROK_PID
    exit 1
fi

echo "✅ Ngrok URL: $NGROK_URL"
echo "📝 Add this webhook URL to inference.net dashboard:"
echo "   $NGROK_URL/webhook"
echo ""

# Start FastAPI
echo "🚀 Starting FastAPI..."
uvicorn api:app --reload 