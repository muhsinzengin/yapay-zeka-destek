"""
Sentiment Analyzer
Analyzes sentiment of user messages (positive, negative, neutral)
"""

import logging
import re

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Simple rule-based sentiment analyzer for Turkish"""

    def __init__(self):
        # Turkish positive words
        self.positive_words = {
            'iyi', 'güzel', 'harika', 'mükemmel', 'süper', 'teşekkür', 
            'teşekkürler', 'sağol', 'sağolun', 'mutlu', 'sevindim', 
            'beğendim', 'memnun', 'başarılı', 'hoş', 'tatlı', 'sevimli',
            'işe yaradı', 'yardımcı', 'faydalı'
        }
        
        # Turkish negative words
        self.negative_words = {
            'kötü', 'berbat', 'rezalet', 'çok kötü', 'hiç', 'olmadı',
            'olmaz', 'problem', 'sorun', 'şikayet', 'kızgın', 'sinir',
            'üzgün', 'mutsuz', 'başarısız', 'işe yaramadı', 'yetersiz',
            'anlamsız', 'saçma', 'aptal', 'gereksiz', 'zaman kaybı'
        }
        
        # Anger indicators for special handling
        self.anger_words = {
            'kızgınım', 'sinirli', 'öfkeli', 'rezalet', 'berbat', 
            'çok kötü', 'aptalca', 'saçmalık'
        }

    def analyze(self, text: str) -> str:
        """
        Analyze sentiment of text
        Returns: 'positive', 'negative', 'angry', or 'neutral'
        """
        if not text:
            return 'neutral'
        
        text_lower = text.lower()
        
        # Check for anger first
        anger_score = sum(1 for word in self.anger_words if word in text_lower)
        if anger_score > 0:
            return 'angry'
        
        # Calculate positive and negative scores
        positive_score = sum(1 for word in self.positive_words if word in text_lower)
        negative_score = sum(1 for word in self.negative_words if word in text_lower)
        
        # Check for negation patterns (e.g., "iyi değil" = not good)
        negation_pattern = r'\b(değil|değilim|değilsin|olmadı|olamaz)\b'
        has_negation = bool(re.search(negation_pattern, text_lower))
        
        if has_negation:
            # Swap scores if negation is present
            positive_score, negative_score = negative_score, positive_score
        
        # Determine sentiment
        if positive_score > negative_score:
            return 'positive'
        elif negative_score > positive_score:
            return 'negative'
        else:
            return 'neutral'

    def get_anger_response(self) -> str:
        """Get appropriate response for angry customers"""
        responses = [
            "Üzgünüm, sizin böyle hissetmenize neden olduğum için. Hemen bir müşteri temsilcisini size bağlıyorum.",
            "Anlıyorum, bu durumun sizin için ne kadar sinir bozucu olduğunu anlıyorum. Size yardımcı olmak için elimden geleni yapacağım.",
            "Haklısınız, bu durumun böyle olmaması gerekiyordu. Sorununuzu en kısa sürede çözmek için buradayım."
        ]
        import random
        return random.choice(responses)
