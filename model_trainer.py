import pandas as pd
import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

def preprocess_text(text):
    """
    Basic preprocessing: lowercasing, removing HTML tags, 
    punctuation, and non-alphanumeric characters.
    """
    if not isinstance(text, str):
        return ""
    # Lowercase
    text = text.lower()
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Remove punctuation and non-alphanumeric (keeping spaces)
    text = re.sub(r'[^\w\s]', '', text)
    return text

def train_model():
    print("Loading split data...")
    try:
        train_df = pd.read_csv('train.csv')
        test_df = pd.read_csv('test.csv')
    except FileNotFoundError:
        print("Error: train.csv or test.csv not found. Please run eda.py first.")
        return

    print("Preprocessing data...")
    # Apply preprocessing (mostly handled by TfidfVectorizer's default tokenization, 
    # but explicit cleaning is good practice and requested)
    X_train = train_df['review'].apply(preprocess_text)
    y_train = train_df['sentiment']
    X_test = test_df['review'].apply(preprocess_text)
    y_test = test_df['sentiment']

    print("Building Pipeline...")
    # Pipeline: TF-IDF (1-2 ngrams) -> Logistic Regression
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
        ('clf', LogisticRegression(random_state=42, max_iter=1000, C=1.0))
    ])

    print("Training model...")
    pipeline.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    print(f"Test Set Accuracy: {accuracy:.4f}")
    print("Classification Report:\n")
    print(report)

    # Save metrics for app usage
    metrics = {'accuracy': accuracy, 'report': report}
    joblib.dump(metrics, 'model_metrics.pkl')

    print("Saving model pipeline...")
    joblib.dump(pipeline, 'sentiment_pipeline.pkl')
    print("Model saved to sentiment_pipeline.pkl")

if __name__ == "__main__":
    train_model()
