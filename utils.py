"""
Shared utilities for the Universal Sentiment Analyzer project.
Centralizes common functionality to eliminate code duplication.
"""

import re
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sentiment_analyzer.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def preprocess_text(text: str) -> str:
    """
    Standardized text preprocessing for both training and inference.
    
    Args:
        text: Raw text input
        
    Returns:
        Cleaned and preprocessed text
    """
    if not isinstance(text, str):
        return ""
    
    # Lowercase
    text = text.lower()
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Remove punctuation and non-alphanumeric (keeping spaces)
    text = re.sub(r'[^\w\s]', '', text)
    
    # Squash multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def validate_text_input(text_input: str) -> Dict[str, Any]:
    """
    Validates text input for sentiment analysis.
    
    Args:
        text_input: Text to validate
        
    Returns:
        Dictionary with 'valid' boolean and optional 'error' message
    """
    if not text_input or len(text_input.strip()) < 4:
        return {
            'valid': False, 
            'error': 'Input too short. Please enter a meaningful sentence.'
        }
    
    # Check for at least some alphabetic characters
    if not re.search('[a-zA-Z]', text_input):
        return {
            'valid': False,
            'error': 'Input must contain text.'
        }
    
    return {'valid': True}

def log_prediction(text: str, prediction: Dict[str, Any], user_id: Optional[str] = None) -> None:
    """
    Log prediction for monitoring and analysis.
    
    Args:
        text: Input text (truncated for privacy)
        prediction: Prediction result
        user_id: Optional user identifier
    """
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'text_length': len(text),
        'text_preview': text[:50] + '...' if len(text) > 50 else text,
        'prediction': prediction.get('label', 'unknown'),
        'confidence': prediction.get('confidence_score', 0),
        'user_id': user_id or 'anonymous'
    }
    
    logger.info(f"Prediction logged: {log_data}")

def ensure_model_exists(model_path: str = 'sentiment_pipeline.pkl') -> bool:
    """
    Check if the trained model exists.
    
    Args:
        model_path: Path to the model file
        
    Returns:
        True if model exists, False otherwise
    """
    exists = os.path.exists(model_path)
    if not exists:
        logger.warning(f"Model file not found at {model_path}")
    return exists

class ModelConfig:
    """Configuration class for model parameters."""
    
    # Sentiment thresholds
    INTERMEDIATE_LOWER = 0.40
    INTERMEDIATE_UPPER = 0.60
    
    # Text validation
    MIN_TEXT_LENGTH = 4
    MAX_TEXT_LENGTH = 10000
    
    # Model settings
    MODEL_PATH = 'sentiment_pipeline.pkl'
    METRICS_PATH = 'model_metrics.pkl'
    
    # Logging
    LOG_PREDICTIONS = True
    LOG_FILE = 'sentiment_analyzer.log'
    
    @classmethod
    def get_sentiment_label(cls, prob_positive: float) -> str:
        """
        Determine sentiment label based on probability.
        
        Args:
            prob_positive: Probability of positive sentiment
            
        Returns:
            Sentiment label: 'Positive', 'Negative', or 'Intermediate'
        """
        if cls.INTERMEDIATE_LOWER <= prob_positive <= cls.INTERMEDIATE_UPPER:
            return "Intermediate"
        elif prob_positive > cls.INTERMEDIATE_UPPER:
            return "Positive"
        else:
            return "Negative"