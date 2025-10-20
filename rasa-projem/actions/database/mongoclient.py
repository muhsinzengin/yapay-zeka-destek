"""
MongoDB Client for logging and data storage
Handles conversation logs, training data, and analytics
"""

import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pymongo import MongoClient, DESCENDING
from pymongo.errors import ConnectionFailure
import logging

logger = logging.getLogger(__name__)


class MongoDBClient:
    """MongoDB client for Rasa chatbot data management"""

    def __init__(self):
        # Get MongoDB connection string from environment
        mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        db_name = os.getenv('MONGODB_DATABASE', 'rasa_chatbot')
        
        try:
            self.client = MongoClient(mongo_uri)
            self.db = self.client[db_name]
            
            # Test connection
            self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
            
            # Create indexes
            self._create_indexes()
            
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def _create_indexes(self):
        """Create necessary indexes for collections"""
        # Index for conversation logs
        self.db.conversations.create_index([("timestamp", DESCENDING)])
        self.db.conversations.create_index("user_id")
        
        # Index for training data
        self.db.training_data.create_index("intent")
        
        # Index for admin codes
        self.db.admin_codes.create_index("expires_at", expireAfterSeconds=0)
        
        # Index for GPT-4 usage
        self.db.gpt4_usage.create_index([("timestamp", DESCENDING)])

    def log_conversation(
        self,
        user_id: str,
        message: str,
        intent: str,
        confidence: float,
        timestamp: datetime
    ):
        """Log conversation message to MongoDB"""
        try:
            self.db.conversations.insert_one({
                "user_id": user_id,
                "message": message,
                "intent": intent,
                "confidence": confidence,
                "timestamp": timestamp
            })
        except Exception as e:
            logger.error(f"Failed to log conversation: {e}")

    def get_user_conversation_count(self, user_id: str) -> int:
        """Get number of conversations for a user"""
        try:
            return self.db.conversations.count_documents({"user_id": user_id})
        except Exception as e:
            logger.error(f"Failed to get conversation count: {e}")
            return 0

    def log_gpt4_usage(
        self,
        user_id: str,
        message: str,
        response: str,
        timestamp: datetime
    ):
        """Log GPT-4 API usage for cost tracking"""
        try:
            self.db.gpt4_usage.insert_one({
                "user_id": user_id,
                "message": message,
                "response": response,
                "timestamp": timestamp,
                # Estimate token count (rough approximation)
                "estimated_tokens": len(message.split()) + len(response.split())
            })
        except Exception as e:
            logger.error(f"Failed to log GPT-4 usage: {e}")

    def store_admin_code(self, code: str, expires_in_minutes: int = 5):
        """Store admin authentication code with expiration"""
        try:
            expires_at = datetime.now() + timedelta(minutes=expires_in_minutes)
            self.db.admin_codes.insert_one({
                "code": code,
                "created_at": datetime.now(),
                "expires_at": expires_at,
                "used": False
            })
        except Exception as e:
            logger.error(f"Failed to store admin code: {e}")

    def verify_admin_code(self, code: str) -> bool:
        """Verify admin authentication code"""
        try:
            result = self.db.admin_codes.find_one({
                "code": code,
                "used": False,
                "expires_at": {"$gt": datetime.now()}
            })
            
            if result:
                # Mark code as used
                self.db.admin_codes.update_one(
                    {"_id": result["_id"]},
                    {"$set": {"used": True}}
                )
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to verify admin code: {e}")
            return False

    def save_training_data(self, data: Dict[str, Any]):
        """Save training data from admin panel"""
        try:
            self.db.training_data.insert_one({
                **data,
                "created_at": datetime.now()
            })
        except Exception as e:
            logger.error(f"Failed to save training data: {e}")

    def get_training_data(self) -> List[Dict[str, Any]]:
        """Get all training data"""
        try:
            return list(self.db.training_data.find().sort("created_at", DESCENDING))
        except Exception as e:
            logger.error(f"Failed to get training data: {e}")
            return []

    def delete_training_data(self, data_id: str):
        """Delete training data by ID"""
        try:
            from bson.objectid import ObjectId
            self.db.training_data.delete_one({"_id": ObjectId(data_id)})
        except Exception as e:
            logger.error(f"Failed to delete training data: {e}")

    def get_statistics(self, period: str = "daily") -> Dict[str, Any]:
        """Get statistics for dashboard"""
        try:
            now = datetime.now()
            
            if period == "daily":
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif period == "weekly":
                start_date = now - timedelta(days=7)
            elif period == "monthly":
                start_date = now - timedelta(days=30)
            elif period == "yearly":
                start_date = now - timedelta(days=365)
            else:
                start_date = datetime.min
            
            # Count conversations
            conversation_count = self.db.conversations.count_documents({
                "timestamp": {"$gte": start_date}
            })
            
            # Count unique users
            unique_users = len(self.db.conversations.distinct("user_id", {
                "timestamp": {"$gte": start_date}
            }))
            
            # Calculate GPT-4 cost (approximate)
            gpt4_records = list(self.db.gpt4_usage.find({
                "timestamp": {"$gte": start_date}
            }))
            
            total_tokens = sum(r.get("estimated_tokens", 0) for r in gpt4_records)
            # GPT-4 Turbo pricing: ~$0.01 per 1K tokens (input) + $0.03 per 1K tokens (output)
            # Rough estimate: $0.02 per 1K tokens average
            estimated_cost = (total_tokens / 1000) * 0.02
            
            return {
                "conversation_count": conversation_count,
                "unique_users": unique_users,
                "gpt4_usage_count": len(gpt4_records),
                "estimated_gpt4_cost": round(estimated_cost, 2),
                "period": period
            }
            
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {}

    def cleanup_old_logs(self, days: int = 30):
        """Delete logs older than specified days"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            result = self.db.conversations.delete_many({
                "timestamp": {"$lt": cutoff_date}
            })
            
            logger.info(f"Deleted {result.deleted_count} old conversation logs")
            
        except Exception as e:
            logger.error(f"Failed to cleanup old logs: {e}")

    def get_live_conversations(self) -> List[Dict[str, Any]]:
        """Get active conversations for live monitoring"""
        try:
            # Get conversations from last hour
            one_hour_ago = datetime.now() - timedelta(hours=1)
            
            pipeline = [
                {"$match": {"timestamp": {"$gte": one_hour_ago}}},
                {"$group": {
                    "_id": "$user_id",
                    "last_message": {"$last": "$message"},
                    "last_timestamp": {"$last": "$timestamp"},
                    "message_count": {"$sum": 1}
                }},
                {"$sort": {"last_timestamp": -1}}
            ]
            
            return list(self.db.conversations.aggregate(pipeline))
            
        except Exception as e:
            logger.error(f"Failed to get live conversations: {e}")
            return []

    def export_conversations_to_nlu(self, output_path: str):
        """Export conversations to NLU training format"""
        try:
            # Get all unique intents and their examples
            pipeline = [
                {"$group": {
                    "_id": "$intent",
                    "examples": {"$addToSet": "$message"}
                }}
            ]
            
            intents = list(self.db.conversations.aggregate(pipeline))
            
            # Generate NLU YAML format
            nlu_data = "version: \"3.1\"\n\nnlu:\n"
            
            for intent in intents:
                if intent["_id"] and intent["examples"]:
                    nlu_data += f"- intent: {intent['_id']}\n"
                    nlu_data += "  examples: |\n"
                    for example in intent["examples"][:50]:  # Limit to 50 examples per intent
                        nlu_data += f"    - {example}\n"
                    nlu_data += "\n"
            
            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(nlu_data)
            
            logger.info(f"Exported conversations to {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to export conversations: {e}")

    def backup_database(self, backup_path: str):
        """Create database backup"""
        try:
            import json
            from bson import json_util
            
            backup_data = {
                "conversations": list(self.db.conversations.find()),
                "training_data": list(self.db.training_data.find()),
                "gpt4_usage": list(self.db.gpt4_usage.find()),
                "backup_timestamp": datetime.now()
            }
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, default=json_util.default, indent=2, ensure_ascii=False)
            
            logger.info(f"Database backup created at {backup_path}")
            
        except Exception as e:
            logger.error(f"Failed to backup database: {e}")

    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")
