#!/bin/bash
# TurabIQ Quick Start Script
# Starts mock backend + prints frontend start instructions

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         🧪 TurabIQ Mock Backend Launcher 🧪                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ ! -f "backend/mock_backend.py" ]; then
    echo "❌ Error: mock_backend.py not found!"
    echo "   Make sure you run this from the TurabIQ project root:"
    echo "   cd /path/to/TurabIQ"
    echo "   bash start_mock.sh"
    exit 1
fi

# Check if FastAPI/Uvicorn are installed
echo "📦 Checking dependencies..."
if ! python -c "import fastapi" 2>/dev/null; then
    echo "   Installing fastapi and uvicorn..."
    pip install fastapi uvicorn --quiet
fi

echo "✓ Dependencies ready"
echo ""

# Start the mock backend
echo "🚀 Starting Mock Backend..."
echo "   WebSocket: ws://localhost:8000/ws"
echo "   REST API:  http://localhost:8000"
echo "   Docs:      http://localhost:8000/docs"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo ""

cd backend
python mock_backend.py &
BACKEND_PID=$!

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "✓ Mock backend running (PID: $BACKEND_PID)"
echo ""
echo "📋 Next: Start the frontend in another terminal:"
echo ""
echo "   cd frontend"
echo "   npm install  # if first time"
echo "   npm run dev"
echo ""
echo "🌐 Then open: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop the backend"
echo ""

wait $BACKEND_PID
