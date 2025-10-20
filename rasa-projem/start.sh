#!/bin/bash
# Startup script for Rasa Chatbot System
# This script starts all required services

echo "🚀 Starting Rasa Chatbot System..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env file with your configuration before proceeding."
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "⚠️  MongoDB is not running. Please start MongoDB first."
    echo "   sudo systemctl start mongodb"
    exit 1
fi

# Create necessary directories
mkdir -p models backups logs

echo "📦 Installing/Updating dependencies..."
pip install -q -r ../requirements.txt

# Check if model exists, if not train one
if [ ! "$(ls -A models/*.tar.gz 2>/dev/null)" ]; then
    echo "🎓 No trained model found. Training initial model..."
    rasa train --quiet
fi

# Start services in background
echo "🌐 Starting Rasa Server..."
rasa run --enable-api --cors "*" --port 5005 > logs/rasa.log 2>&1 &
RASA_PID=$!

echo "⚙️  Starting Action Server..."
rasa run actions --port 5055 > logs/actions.log 2>&1 &
ACTION_PID=$!

echo "🖥️  Starting Flask API Server..."
python app.py > logs/flask.log 2>&1 &
FLASK_PID=$!

# Wait a bit for servers to start
sleep 5

# Check if all services are running
if ! kill -0 $RASA_PID 2>/dev/null; then
    echo "❌ Rasa Server failed to start. Check logs/rasa.log"
    exit 1
fi

if ! kill -0 $ACTION_PID 2>/dev/null; then
    echo "❌ Action Server failed to start. Check logs/actions.log"
    exit 1
fi

if ! kill -0 $FLASK_PID 2>/dev/null; then
    echo "❌ Flask API Server failed to start. Check logs/flask.log"
    exit 1
fi

echo ""
echo "✅ All services started successfully!"
echo ""
echo "📍 Service URLs:"
echo "   Rasa Server:      http://localhost:5005"
echo "   Action Server:    http://localhost:5055"
echo "   Flask API:        http://localhost:5000"
echo "   Webchat:          http://localhost:5000/webchat/index.html"
echo "   Admin Panel:      http://localhost:5000/admin/dashboard.html"
echo "   Test Page:        http://localhost:5000/test_sayfa.html"
echo ""
echo "📝 Process IDs:"
echo "   Rasa:    $RASA_PID"
echo "   Actions: $ACTION_PID"
echo "   Flask:   $FLASK_PID"
echo ""
echo "🛑 To stop all services, run: ./stop.sh"
echo "📋 To view logs, check the logs/ directory"

# Save PIDs to file for stop script
echo $RASA_PID > logs/rasa.pid
echo $ACTION_PID > logs/actions.pid
echo $FLASK_PID > logs/flask.pid

# Keep script running
echo ""
echo "Press Ctrl+C to view logs or use ./stop.sh to stop all services"
tail -f logs/*.log
