"""
GPT-4 Fallback Handler
Fallback to GPT-4 Turbo API when Rasa confidence is low
"""

import os
import logging
from typing import Optional
import requests

logger = logging.getLogger(__name__)


class GPT4Fallback:
    """Handle GPT-4 Turbo fallback for low-confidence responses"""

    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY', '')
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-4-turbo-preview"
        
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not set - GPT-4 fallback disabled")

    def get_response(self, message: str, user_id: str) -> str:
        """Get response from GPT-4 Turbo"""
        if not self.api_key:
            return "Üzgünüm, şu anda bu konuda size yardımcı olamıyorum. Lütfen sorunuzu farklı şekilde ifade etmeyi deneyin."
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "Sen yardımcı ve profesyonel bir müşteri destek asistanısın. Türkçe konuşuyorsun. Kısa, net ve yardımcı yanıtlar veriyorsun."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result['choices'][0]['message']['content']
                logger.info(f"GPT-4 response generated for user {user_id}")
                return answer
            else:
                logger.error(f"GPT-4 API error: {response.status_code} - {response.text}")
                return "Üzgünüm, bir hata oluştu. Lütfen daha sonra tekrar deneyin."
                
        except requests.exceptions.Timeout:
            logger.error("GPT-4 API timeout")
            return "Üzgünüm, yanıt vermem biraz uzun sürdü. Lütfen tekrar deneyin."
            
        except Exception as e:
            logger.error(f"GPT-4 API error: {e}")
            return "Üzgünüm, bir hata oluştu. Lütfen daha sonra tekrar deneyin."
