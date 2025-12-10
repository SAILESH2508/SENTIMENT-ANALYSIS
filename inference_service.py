import joblib
import re

# Load the model once at module level to avoid reloading on every request if imported
try:
    pipeline = joblib.load('sentiment_pipeline.pkl')
except:
    pipeline = None

def preprocess_text(text):
    """
    Same preprocessing as training.
    Duplicate definition to keep file standalone/modular as requested.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text

def predict_sentiment(text_input):
    """
    Predicts sentiment for a given text input.
    Returns dictionary with label and confidence score.
    """
    global pipeline
    if pipeline is None:
        try:
            pipeline = joblib.load('sentiment_pipeline.pkl')
        except FileNotFoundError:
            return {'error': 'Model not found. Please train the model first.'}

    # 1. Validation Layer
    if not text_input or len(text_input.strip()) < 4:
        return {'error': 'Input too short. Please enter a meaningful sentence.'}
    
    # Check for at least some alphabetic characters to avoid "12345" or "...."
    if not re.search('[a-zA-Z]', text_input):
         return {'error': 'Input must contain text.'}

    processed_text = preprocess_text(text_input)
    
    # Predict Probability
    # classes_ are usually [0, 1] for [Negative, Positive]
    # predict_proba returns [prob_0, prob_1]
    probs = pipeline.predict_proba([processed_text])[0]
    prob_pos = probs[1]
    
    # 2. Intermediate Logic
    if 0.40 <= prob_pos <= 0.60:
        label = "Intermediate"
        confidence_score = prob_pos # Keep the raw probability for display
    elif prob_pos > 0.60:
        label = "Positive"
        confidence_score = prob_pos
    else:
        label = "Negative"
        confidence_score = probs[0] # Confidence in being Negative
    
    return {
        'label': label,
        'confidence_score': float(confidence_score)
    }

if __name__ == "__main__":
    # Test block
    test_text = "I absolutely loved this movie! It was fantastic."
    print(f"Test Input: {test_text}")
    print(f"Result: {predict_sentiment(test_text)}")
