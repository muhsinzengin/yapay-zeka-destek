"""
Telegram Notifier
Sends notifications for new customers and admin authentication codes
"""

import os
import logging
from telegram import Bot
from telegram.error import TelegramError

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Handle Telegram notifications"""

    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        self.admin_chat_id = os.getenv('TELEGRAM_ADMIN_CHAT_ID', '')
        
        if self.bot_token:
            try:
                self.bot = Bot(token=self.bot_token)
            except Exception as e:
                logger.error(f"Failed to initialize Telegram bot: {e}")
                self.bot = None
        else:
            logger.warning("TELEGRAM_BOT_TOKEN not set")
            self.bot = None

    def notify_new_customer(self, user_id: str, message: str):
        """Send notification when new customer starts conversation"""
        if not self.bot or not self.admin_chat_id:
            logger.warning("Telegram bot not configured")
            return
        
        try:
            notification = (
                f"🆕 Yeni Müşteri!\n\n"
                f"👤 Kullanıcı: {user_id}\n"
                f"💬 İlk Mesaj: {message[:100]}..."
            )
            
            self.bot.send_message(
                chat_id=self.admin_chat_id,
                text=notification
            )
            logger.info(f"Sent new customer notification for {user_id}")
            
        except TelegramError as e:
            logger.error(f"Failed to send Telegram notification: {e}")

    def send_admin_code(self, code: str):
        """Send 6-digit authentication code to admin"""
        if not self.bot or not self.admin_chat_id:
            logger.warning("Telegram bot not configured")
            return
        
        try:
            message = (
                f"🔐 Admin Giriş Kodu\n\n"
                f"Kodunuz: {code}\n\n"
                f"⏱ Bu kod 5 dakika geçerlidir."
            )
            
            self.bot.send_message(
                chat_id=self.admin_chat_id,
                text=message
            )
            logger.info("Sent admin authentication code")
            
        except TelegramError as e:
            logger.error(f"Failed to send admin code: {e}")

    def notify_admin_intervention_needed(self, user_id: str, conversation_summary: str):
        """Notify admin when intervention is needed"""
        if not self.bot or not self.admin_chat_id:
            logger.warning("Telegram bot not configured")
            return
        
        try:
            message = (
                f"⚠️ Müdahale Gerekli\n\n"
                f"👤 Kullanıcı: {user_id}\n"
                f"📝 Özet: {conversation_summary}"
            )
            
            self.bot.send_message(
                chat_id=self.admin_chat_id,
                text=message
            )
            logger.info(f"Sent intervention notification for {user_id}")
            
        except TelegramError as e:
            logger.error(f"Failed to send intervention notification: {e}")
