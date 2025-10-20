#!/bin/bash
# Stop script for Rasa Chatbot System

echo "🛑 Stopping Rasa Chatbot System..."

# Read PIDs from files
if [ -f logs/rasa.pid ]; then
    RASA_PID=$(cat logs/rasa.pid)
    if kill -0 $RASA_PID 2>/dev/null; then
        echo "   Stopping Rasa Server (PID: $RASA_PID)..."
        kill $RASA_PID
    fi
    rm logs/rasa.pid
fi

if [ -f logs/actions.pid ]; then
    ACTION_PID=$(cat logs/actions.pid)
    if kill -0 $ACTION_PID 2>/dev/null; then
        echo "   Stopping Action Server (PID: $ACTION_PID)..."
        kill $ACTION_PID
    fi
    rm logs/actions.pid
fi

if [ -f logs/flask.pid ]; then
    FLASK_PID=$(cat logs/flask.pid)
    if kill -0 $FLASK_PID 2>/dev/null; then
        echo "   Stopping Flask API Server (PID: $FLASK_PID)..."
        kill $FLASK_PID
    fi
    rm logs/flask.pid
fi

# Kill any remaining processes
pkill -f "rasa run"
pkill -f "python app.py"

echo "✅ All services stopped"
