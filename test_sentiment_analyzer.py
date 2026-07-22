"""
Comprehensive test suite for the Universal Sentiment Analyzer.
"""

import pytest
import pandas as pd
import os
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock
from utils import preprocess_text, validate_text_input, ModelConfig
from enhanced_inference_service import SentimentAnalyzer
from monitoring import PerformanceMonitor


class TestUtils:
    """Test utility functions."""

    def test_preprocess_text_basic(self):
        """Test basic text preprocessing."""
        text = "This is a GREAT movie! <br> Really enjoyed it."
        expected = "this is a great movie really enjoyed it"
        assert preprocess_text(text) == expected

    def test_preprocess_text_empty(self):
        """Test preprocessing with empty/invalid input."""
        assert preprocess_text("") == ""
        assert preprocess_text(None) == ""
        assert preprocess_text(123) == ""

    def test_preprocess_text_html_tags(self):
        """Test HTML tag removal."""
        text = "<div>Hello <span>world</span>!</div>"
        expected = "hello world"
        assert preprocess_text(text) == expected

    def test_validate_text_input_valid(self):
        """Test validation with valid input."""
        result = validate_text_input("This is a valid sentence.")
        assert result["valid"] is True
        assert "error" not in result

    def test_validate_text_input_too_short(self):
        """Test validation with too short input."""
        result = validate_text_input("Hi")
        assert result["valid"] is False
        assert "too short" in result["error"].lower()

    def test_validate_text_input_no_letters(self):
        """Test validation with no alphabetic characters."""
        result = validate_text_input("12345!@#$%")
        assert result["valid"] is False
        assert "must contain text" in result["error"].lower()

    def test_model_config_sentiment_labels(self):
        """Test sentiment label assignment."""
        assert ModelConfig.get_sentiment_label(0.3) == "Negative"
        assert ModelConfig.get_sentiment_label(0.5) == "Intermediate"
        assert ModelConfig.get_sentiment_label(0.7) == "Positive"


class TestSentimentAnalyzer:
    """Test the enhanced sentiment analyzer."""

    @pytest.fixture
    def mock_pipeline(self):
        """Create a mock pipeline for testing."""
        pipeline = Mock()
        pipeline.predict_proba.return_value = [[0.3, 0.7]]  # Mock probabilities

        # Mock named_steps for get_model_info
        mock_clf = Mock()
        mock_clf.__class__.__name__ = "LogisticRegression"
        mock_tfidf = Mock()
        mock_tfidf.__class__.__name__ = "TfidfVectorizer"
        mock_tfidf.get_feature_names_out.return_value = ["word1", "word2"]

        pipeline.named_steps = {"clf": mock_clf, "tfidf": mock_tfidf}
        return pipeline

    @pytest.fixture
    def analyzer_with_mock_pipeline(self, mock_pipeline):
        """Create analyzer with mocked pipeline."""
        with patch(
            "enhanced_inference_service.joblib.load", return_value=mock_pipeline
        ):
            with patch(
                "enhanced_inference_service.ensure_model_exists", return_value=True
            ):
                analyzer = SentimentAnalyzer()
                analyzer.pipeline = mock_pipeline
                return analyzer

    def test_predict_sentiment_valid_input(self, analyzer_with_mock_pipeline):
        """Test prediction with valid input."""
        result = analyzer_with_mock_pipeline.predict_sentiment("This is a great movie!")

        assert "error" not in result
        assert result["label"] == "Positive"
        assert "confidence_score" in result
        assert "probabilities" in result

    def test_predict_sentiment_invalid_input(self, analyzer_with_mock_pipeline):
        """Test prediction with invalid input."""
        result = analyzer_with_mock_pipeline.predict_sentiment("Hi")
        assert "error" in result
        assert "too short" in result["error"].lower()

    def test_predict_sentiment_caching(self, analyzer_with_mock_pipeline):
        """Test prediction caching functionality."""
        text = "This is a test sentence for caching."

        # First prediction
        result1 = analyzer_with_mock_pipeline.predict_sentiment(text)

        # Second prediction (should use cache)
        result2 = analyzer_with_mock_pipeline.predict_sentiment(text)

        assert result1 == result2
        # Pipeline should only be called once due to caching
        assert analyzer_with_mock_pipeline.pipeline.predict_proba.call_count == 1

    def test_predict_batch(self, analyzer_with_mock_pipeline):
        """Test batch prediction."""
        texts = ["Great movie!", "Terrible film.", "It was okay."]
        results = analyzer_with_mock_pipeline.predict_batch(texts)

        assert len(results) == 3
        for result in results:
            assert "label" in result or "error" in result

    def test_get_model_info(self, analyzer_with_mock_pipeline):
        """Test model info retrieval."""
        info = analyzer_with_mock_pipeline.get_model_info()

        assert "error" not in info
        assert "model_type" in info
        assert "cache_size" in info

    def test_clear_cache(self, analyzer_with_mock_pipeline):
        """Test cache clearing."""
        # Add something to cache
        analyzer_with_mock_pipeline.predict_sentiment("Test sentence")
        assert len(analyzer_with_mock_pipeline.prediction_cache) > 0

        # Clear cache
        analyzer_with_mock_pipeline.clear_cache()
        assert len(analyzer_with_mock_pipeline.prediction_cache) == 0


class TestPerformanceMonitor:
    """Test performance monitoring functionality."""

    @pytest.fixture
    def temp_log_file(self):
        """Create a temporary log file for testing."""
        from datetime import datetime, timedelta

        now = datetime.now()
        t1 = (now - timedelta(days=1)).isoformat()
        t2 = (now - timedelta(days=2)).isoformat()
        t3 = (now - timedelta(days=3)).isoformat()

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            # Write sample log entries with dynamic timestamps
            sample_logs = [
                f'2026-07-20 10:00:00,000 - INFO - Prediction logged: {{"timestamp": "{t1}", "text_length": 50, "text_preview": "This is a great movie...", "prediction": "Positive", "confidence": 0.85, "user_id": "user1"}}',
                f'2026-07-20 11:00:00,000 - INFO - Prediction logged: {{"timestamp": "{t2}", "text_length": 30, "text_preview": "Bad movie...", "prediction": "Negative", "confidence": 0.75, "user_id": "user2"}}',
                f'2026-07-20 12:00:00,000 - INFO - Prediction logged: {{"timestamp": "{t3}", "text_length": 40, "text_preview": "It was okay...", "prediction": "Intermediate", "confidence": 0.55, "user_id": "user1"}}',
            ]
            for log in sample_logs:
                f.write(log + "\n")
            f.flush()

        yield f.name

        # Cleanup
        os.unlink(f.name)

    def test_parse_prediction_logs(self, temp_log_file):
        """Test log parsing functionality."""
        monitor = PerformanceMonitor(temp_log_file)
        df = monitor.parse_prediction_logs(
            days_back=30
        )  # Large window to catch test data

        assert not df.empty
        assert len(df) == 3
        assert "timestamp" in df.columns
        assert "prediction" in df.columns
        assert "confidence" in df.columns

    def test_generate_performance_report(self, temp_log_file):
        """Test performance report generation."""
        monitor = PerformanceMonitor(temp_log_file)
        report = monitor.generate_performance_report(days_back=30)

        assert "error" not in report
        assert "total_predictions" in report
        assert "sentiment_distribution" in report
        assert "confidence_statistics" in report
        assert report["total_predictions"] == 3

    def test_detect_anomalies(self, temp_log_file):
        """Test anomaly detection."""
        monitor = PerformanceMonitor(temp_log_file)
        anomalies = monitor.detect_anomalies(days_back=30)

        # Should return a list (may be empty for our small test dataset)
        assert isinstance(anomalies, list)


class TestIntegration:
    """Integration tests for the complete system."""

    @pytest.fixture
    def sample_csv_file(self):
        """Create a sample CSV file for testing."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            df = pd.DataFrame(
                {
                    "text": [
                        "This is a great movie!",
                        "Terrible film, waste of time.",
                        "It was okay, nothing special.",
                        "Amazing cinematography and acting!",
                    ]
                }
            )
            df.to_csv(f.name, index=False)

        yield f.name
        os.unlink(f.name)

    @patch("enhanced_inference_service.joblib.load")
    @patch("enhanced_inference_service.ensure_model_exists")
    def test_end_to_end_prediction(self, mock_exists, mock_load):
        """Test end-to-end prediction workflow."""
        # Setup mocks
        mock_exists.return_value = True
        mock_pipeline = Mock()
        mock_pipeline.predict_proba.return_value = [[0.2, 0.8]]
        mock_load.return_value = mock_pipeline

        # Create analyzer
        analyzer = SentimentAnalyzer()

        # Test prediction
        result = analyzer.predict_sentiment("This is a fantastic movie!")

        assert "error" not in result
        assert result["label"] == "Positive"
        assert "confidence_score" in result


# Test configuration
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment."""
    # Ensure test logs don't interfere with real logs
    import logging

    logging.getLogger().handlers = []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
