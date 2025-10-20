"""
Rasa Custom Actions
Handles MongoDB integration, Telegram notifications, sentiment analysis,
and conversation logging.
"""

from typing import Any, Text, Dict, List
import random
import string
import os
from datetime import datetime
import logging

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Import custom modules
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database.mongoclient import MongoDBClient
from telegram_notifier import TelegramNotifier
from sentiment_analyzer import SentimentAnalyzer
from gpt4_fallback import GPT4Fallback

logger = logging.getLogger(__name__)

# Initialize services
mongo_client = MongoDBClient()
telegram_notifier = TelegramNotifier()
sentiment_analyzer = SentimentAnalyzer()
gpt4_fallback = GPT4Fallback()


class ActionLogConversation(Action):
    """Log conversation to MongoDB"""

    def name(self) -> Text:
        return "action_log_conversation"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        user_id = tracker.sender_id
        message = tracker.latest_message.get('text', '')
        intent = tracker.latest_message.get('intent', {}).get('name', '')
        confidence = tracker.latest_message.get('intent', {}).get('confidence', 0)
        
        # Log to MongoDB
        mongo_client.log_conversation(
            user_id=user_id,
            message=message,
            intent=intent,
            confidence=confidence,
            timestamp=datetime.now()
        )
        
        return []


class ActionAnalyzeSentiment(Action):
    """Analyze sentiment of user message"""

    def name(self) -> Text:
        return "action_analyze_sentiment"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        message = tracker.latest_message.get('text', '')
        sentiment = sentiment_analyzer.analyze(message)
        
        # Store sentiment in slot
        return [SlotSet("duygu", sentiment)]


class ActionNotifyTelegram(Action):
    """Send Telegram notification for new customer"""

    def name(self) -> Text:
        return "action_notify_telegram"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        user_id = tracker.sender_id
        message = tracker.latest_message.get('text', '')
        
        # Check if this is a new conversation
        conversation_count = mongo_client.get_user_conversation_count(user_id)
        
        if conversation_count <= 1:
            # New customer - send Telegram notification
            telegram_notifier.notify_new_customer(user_id, message)
        
        return []


class ActionFallbackGPT4(Action):
    """Fallback to GPT-4 Turbo when confidence is low"""

    def name(self) -> Text:
        return "action_fallback_gpt4"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        message = tracker.latest_message.get('text', '')
        user_id = tracker.sender_id
        
        # Get GPT-4 response
        response = gpt4_fallback.get_response(message, user_id)
        
        # Log GPT-4 usage for cost tracking
        mongo_client.log_gpt4_usage(
            user_id=user_id,
            message=message,
            response=response,
            timestamp=datetime.now()
        )
        
        dispatcher.utter_message(text=response)
        
        return []


class ActionAdminAuthenticate(Action):
    """Authenticate admin with 6-digit code via Telegram"""

    def name(self) -> Text:
        return "action_admin_authenticate"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        # Generate 6-digit code
        code = ''.join(random.choices(string.digits, k=6))
        
        # Send code via Telegram
        telegram_notifier.send_admin_code(code)
        
        # Store code in MongoDB with expiration
        mongo_client.store_admin_code(code, expires_in_minutes=5)
        
        dispatcher.utter_message(text=f"6 haneli kod Telegram'a gönderildi: {code}")
        
        return []


class ActionSaveTrainingData(Action):
    """Save training data from admin panel to NLU"""

    def name(self) -> Text:
        return "action_save_training_data"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        admin_data = tracker.get_slot("admin_veri")
        
        if admin_data:
            # Parse and save training data
            mongo_client.save_training_data(admin_data)
            dispatcher.utter_message(text="Eğitim verisi kaydedildi.")
        
        return []
