#!/bin/bash

# Start script for Anton AI Companion

echo "🤖 Starting Anton AI Companion..."
echo ""

# Check for HF_TOKEN
if [ -z "$HF_TOKEN" ]; then
    echo "❌ Error: HF_TOKEN not set!"
    echo "Please set your HuggingFace token:"
    echo "export HF_TOKEN='your_token_here'"
    exit 1
fi

# Start backend API server
echo "🚀 Starting backend API server (port 8000)..."
python api_server.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 2

# Start frontend dev server
echo "🎨 Starting Next.js frontend (port 3000)..."
npm run dev &
FRONTEND_PID=$!

# Wait for user to terminate
echo ""
echo "✅ Anton is running!"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop..."

wait
