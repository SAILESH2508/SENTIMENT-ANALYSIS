import pandas as pd
import joblib

try:
    import yaml
except ImportError:
    yaml = None

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from utils import preprocess_text, ModelConfig
import logging

logger = logging.getLogger(__name__)


def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from YAML file."""
    if yaml is None:
        return {}
    try:
        with open(config_path, "r") as file:
            return yaml.safe_load(file) or {}
    except FileNotFoundError:
        logger.warning(f"Config file {config_path} not found, using defaults")
        return {}
    except Exception:
        return {}


def train_model():
    """Train the sentiment analysis model with enhanced configuration and metrics."""
    print("Loading configuration...")
    config = load_config()

    print("Loading split data...")
    try:
        train_df = pd.read_csv("data/train.csv")
        test_df = pd.read_csv("data/test.csv")
    except FileNotFoundError:
        print(
            "Error: train.csv or test.csv not found in data/ directory. Please run eda.py first."
        )
        return

    print("Preprocessing data...")
    # Use shared preprocessing function
    X_train = train_df["review"].apply(preprocess_text)
    y_train = train_df["sentiment"]
    X_test = test_df["review"].apply(preprocess_text)
    y_test = test_df["sentiment"]

    print("Building Pipeline...")
    # Get training parameters from config
    training_config = config.get("model", {}).get("training", {})

    pipeline = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=tuple(training_config.get("ngram_range", [1, 2]))
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    random_state=training_config.get("random_state", 42),
                    max_iter=training_config.get("max_iter", 1000),
                    C=training_config.get("c_value", 1.0),
                ),
            ),
        ]
    )

    print("Training model...")
    pipeline.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # Generate comprehensive metrics
    metrics = {
        "accuracy": accuracy,
        "classification_report": classification_report(
            y_test, y_pred, output_dict=True
        ),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "feature_count": len(pipeline.named_steps["tfidf"].get_feature_names_out()),
        "training_samples": len(X_train),
        "test_samples": len(X_test),
    }

    print(f"Model Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save model and metrics
    model_path = config.get("model", {}).get("path", ModelConfig.MODEL_PATH)
    metrics_path = config.get("model", {}).get("metrics_path", ModelConfig.METRICS_PATH)

    print(f"Saving model to {model_path}...")
    joblib.dump(pipeline, model_path)

    print(f"Saving metrics to {metrics_path}...")
    joblib.dump(metrics, metrics_path)

    print("Training completed successfully!")
    return pipeline, metrics

    print("Evaluating model...")
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"Test Set Accuracy: {accuracy:.4f}")
    print("Classification Report:\n")
    print(report)

    # Save metrics for app usage
    metrics = {"accuracy": accuracy, "report": report}
    joblib.dump(metrics, "model_metrics.pkl")

    print("Saving model pipeline...")
    joblib.dump(pipeline, "sentiment_pipeline.pkl")
    print("Model saved to sentiment_pipeline.pkl")


if __name__ == "__main__":
    train_model()
