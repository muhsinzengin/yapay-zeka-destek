"""
Flask API Server
Provides backend API for admin panel, handles training, statistics, and live chat
"""

import os
import sys
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import logging

# Add actions directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'actions'))

from actions.database.mongoclient import MongoDBClient

app = Flask(__name__)
CORS(app)  # Enable CORS for admin panel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MongoDB client
mongo_client = MongoDBClient()


# Serve admin panel files
@app.route('/admin/<path:filename>')
def serve_admin(filename):
    """Serve admin panel static files"""
    return send_from_directory('admin_panel', filename)


@app.route('/webchat/<path:filename>')
def serve_webchat(filename):
    """Serve webchat static files"""
    return send_from_directory('webchat', filename)


# Health check endpoints
@app.route('/api/health/mongo')
def health_mongo():
    """Check MongoDB connection health"""
    try:
        mongo_client.client.admin.command('ping')
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        logger.error(f"MongoDB health check failed: {e}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


@app.route('/api/health/telegram')
def health_telegram():
    """Check Telegram configuration"""
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
    if telegram_token:
        return jsonify({"status": "configured"}), 200
    return jsonify({"status": "not_configured"}), 200


# Statistics endpoints
@app.route('/api/statistics')
def get_statistics():
    """Get statistics for specified period"""
    period = request.args.get('period', 'daily')
    
    try:
        stats = mongo_client.get_statistics(period)
        return jsonify(stats), 200
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({"error": str(e)}), 500


# Training data endpoints
@app.route('/api/training-data', methods=['GET'])
def get_training_data():
    """Get all training data"""
    try:
        data = mongo_client.get_training_data()
        # Convert ObjectId to string for JSON serialization
        for item in data:
            item['_id'] = str(item['_id'])
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error getting training data: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/training-data', methods=['POST'])
def add_training_data():
    """Add new training data"""
    try:
        data = request.json
        mongo_client.save_training_data(data)
        return jsonify({"status": "success"}), 201
    except Exception as e:
        logger.error(f"Error adding training data: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/training-data/<data_id>', methods=['DELETE'])
def delete_training_data(data_id):
    """Delete training data by ID"""
    try:
        mongo_client.delete_training_data(data_id)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.error(f"Error deleting training data: {e}")
        return jsonify({"error": str(e)}), 500


# Live conversation endpoints
@app.route('/api/live-conversations')
def get_live_conversations():
    """Get active conversations"""
    try:
        conversations = mongo_client.get_live_conversations()
        return jsonify(conversations), 200
    except Exception as e:
        logger.error(f"Error getting live conversations: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/conversation/<user_id>')
def get_conversation(user_id):
    """Get conversation history for specific user"""
    try:
        messages = list(mongo_client.db.conversations.find(
            {"user_id": user_id}
        ).sort("timestamp", 1).limit(100))
        
        # Convert ObjectId to string
        for msg in messages:
            msg['_id'] = str(msg['_id'])
            msg['timestamp'] = msg['timestamp'].isoformat()
        
        return jsonify(messages), 200
    except Exception as e:
        logger.error(f"Error getting conversation: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/intervention', methods=['POST'])
def send_intervention():
    """Admin intervention in live chat"""
    try:
        data = request.json
        user_id = data.get('user_id')
        message = data.get('message')
        
        # Log admin intervention
        mongo_client.db.conversations.insert_one({
            "user_id": user_id,
            "message": message,
            "sender": "admin",
            "timestamp": datetime.now(),
            "intervention": True
        })
        
        # TODO: Send message to user via websocket or other real-time mechanism
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.error(f"Error sending intervention: {e}")
        return jsonify({"error": str(e)}), 500


# Model training endpoint
@app.route('/api/train-model', methods=['POST'])
def train_model():
    """Trigger model training"""
    try:
        import subprocess
        
        # Export conversations to NLU format
        nlu_path = os.path.join(os.path.dirname(__file__), 'data', 'nlu.yml')
        mongo_client.export_conversations_to_nlu(nlu_path)
        
        # Trigger Rasa training (async)
        subprocess.Popen([
            'rasa', 'train',
            '--domain', 'domain.yml',
            '--data', 'data',
            '--config', 'config.yml'
        ], cwd=os.path.dirname(__file__))
        
        logger.info("Model training started")
        return jsonify({"status": "training_started"}), 200
    except Exception as e:
        logger.error(f"Error training model: {e}")
        return jsonify({"error": str(e)}), 500


# Admin authentication
@app.route('/api/admin/request-code', methods=['POST'])
def request_admin_code():
    """Request admin authentication code"""
    try:
        import random
        import string
        from actions.telegram_notifier import TelegramNotifier
        
        # Generate 6-digit code
        code = ''.join(random.choices(string.digits, k=6))
        
        # Store in database
        mongo_client.store_admin_code(code, expires_in_minutes=5)
        
        # Send via Telegram
        notifier = TelegramNotifier()
        notifier.send_admin_code(code)
        
        return jsonify({"status": "code_sent"}), 200
    except Exception as e:
        logger.error(f"Error requesting admin code: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/admin/verify-code', methods=['POST'])
def verify_admin_code():
    """Verify admin authentication code"""
    try:
        data = request.json
        code = data.get('code')
        
        if mongo_client.verify_admin_code(code):
            # TODO: Generate and return session token
            return jsonify({"status": "verified", "token": "session_token"}), 200
        else:
            return jsonify({"status": "invalid"}), 401
    except Exception as e:
        logger.error(f"Error verifying admin code: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
