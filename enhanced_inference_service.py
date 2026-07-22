"""
Enhanced inference service with caching, better error handling, and monitoring.
"""

import joblib
import yaml
from typing import Dict, Any, Optional
from cachetools import TTLCache
import hashlib
from utils import (
    preprocess_text,
    validate_text_input,
    log_prediction,
    ensure_model_exists,
    ModelConfig,
)
import logging

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Enhanced sentiment analyzer with caching and configuration management."""

    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the analyzer with configuration."""
        self.config = self._load_config(config_path)
        self.pipeline = None
        self.model_config = ModelConfig()

        # Initialize prediction cache
        cache_ttl = self.config.get("performance", {}).get("cache_ttl_seconds", 3600)
        self.prediction_cache = TTLCache(maxsize=1000, ttl=cache_ttl)

        self._load_model()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return {}
        except yaml.YAMLError as e:
            logger.error(f"Error parsing config file: {e}")
            return {}

    def _load_model(self) -> None:
        """Load the trained model pipeline."""
        model_path = self.config.get("model", {}).get("path", "sentiment_pipeline.pkl")

        if not ensure_model_exists(model_path):
            logger.error(f"Model file not found: {model_path}")
            return

        try:
            self.pipeline = joblib.load(model_path)
            logger.info(f"Model loaded successfully from {model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.pipeline = None

    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for text input."""
        return hashlib.md5(text.encode()).hexdigest()

    def predict_sentiment(
        self, text_input: str, use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Predict sentiment for given text with caching and enhanced error handling.

        Args:
            text_input: Text to analyze
            use_cache: Whether to use prediction cache

        Returns:
            Dictionary with prediction results or error information
        """
        # Validate input
        validation_result = validate_text_input(text_input)
        if not validation_result["valid"]:
            return {"error": validation_result["error"]}

        # Check cache first
        if use_cache and self.config.get("performance", {}).get(
            "cache_predictions", True
        ):
            cache_key = self._get_cache_key(text_input)
            if cache_key in self.prediction_cache:
                logger.info("Returning cached prediction")
                return self.prediction_cache[cache_key]

        # Check if model is loaded
        if self.pipeline is None:
            return {"error": "Model not available. Please train the model first."}

        try:
            # Preprocess text
            processed_text = preprocess_text(text_input)

            # Get prediction probabilities
            probs = self.pipeline.predict_proba([processed_text])[0]
            prob_positive = probs[1]  # Probability of positive class

            # Determine label using configuration
            thresholds = self.config.get("model", {}).get("thresholds", {})
            lower_threshold = thresholds.get(
                "intermediate_lower", ModelConfig.INTERMEDIATE_LOWER
            )
            upper_threshold = thresholds.get(
                "intermediate_upper", ModelConfig.INTERMEDIATE_UPPER
            )

            if lower_threshold <= prob_positive <= upper_threshold:
                label = "Intermediate"
                confidence_score = prob_positive
            elif prob_positive > upper_threshold:
                label = "Positive"
                confidence_score = prob_positive
            else:
                label = "Negative"
                confidence_score = probs[0]  # Confidence in negative class

            result = {
                "label": label,
                "confidence_score": confidence_score,
                "probabilities": {
                    "positive": float(prob_positive),
                    "negative": float(probs[0]),
                },
                "processed_text_length": len(processed_text),
            }

            # Cache the result
            if use_cache and self.config.get("performance", {}).get(
                "cache_predictions", True
            ):
                self.prediction_cache[cache_key] = result

            # Log prediction if enabled
            if self.config.get("logging", {}).get("log_predictions", True):
                log_prediction(text_input, result)

            return result

        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return {"error": f"Prediction failed: {str(e)}"}

    def predict_batch(self, texts: list) -> list:
        """
        Predict sentiment for multiple texts efficiently.

        Args:
            texts: List of texts to analyze

        Returns:
            List of prediction results
        """
        results = []
        batch_size = self.config.get("performance", {}).get("batch_size", 100)

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            batch_results = [self.predict_sentiment(text) for text in batch]
            results.extend(batch_results)

            logger.info(
                f"Processed batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}"
            )

        return results

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        if self.pipeline is None:
            return {"error": "Model not loaded"}

        try:
            # Try to load model metrics if available
            metrics_path = self.config.get("model", {}).get(
                "metrics_path", "model_metrics.pkl"
            )
            metrics = {}
            try:
                metrics = joblib.load(metrics_path)
            except FileNotFoundError:
                logger.warning(f"Model metrics file not found: {metrics_path}")

            return {
                "model_type": type(self.pipeline.named_steps["clf"]).__name__,
                "vectorizer_type": type(self.pipeline.named_steps["tfidf"]).__name__,
                "feature_count": len(
                    self.pipeline.named_steps["tfidf"].get_feature_names_out()
                )
                if hasattr(self.pipeline.named_steps["tfidf"], "get_feature_names_out")
                else "Unknown",
                "cache_size": len(self.prediction_cache),
                "metrics": metrics,
            }
        except Exception as e:
            logger.error(f"Error getting model info: {e}")
            return {"error": f"Failed to get model info: {str(e)}"}

    def clear_cache(self) -> None:
        """Clear the prediction cache."""
        self.prediction_cache.clear()
        logger.info("Prediction cache cleared")


# Global analyzer instance
_analyzer = None


def get_analyzer() -> SentimentAnalyzer:
    """Get or create the global analyzer instance."""
    global _analyzer
    if _analyzer is None:
        _analyzer = SentimentAnalyzer()
    return _analyzer


# Backward compatibility functions
def predict_sentiment(text_input: str) -> Dict[str, Any]:
    """Backward compatible prediction function."""
    return get_analyzer().predict_sentiment(text_input)
