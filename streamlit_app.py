"""
Streamlit Cloud optimized version of the Universal Sentiment Analyzer
This version works without the enhanced inference service for cloud deployment
"""

import streamlit as st
import joblib
import re
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import requests
from bs4 import BeautifulSoup

# --- Page Configuration ---
st.set_page_config(
    page_title="Universal Sentiment Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load Model ---
@st.cache_resource
def load_model():
    """Load the sentiment analysis model"""
    try:
        if os.path.exists('sentiment_pipeline.pkl'):
            return joblib.load('sentiment_pipeline.pkl')
        else:
            st.error("Model not found. Please ensure sentiment_pipeline.pkl is in the repository.")
            return None
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# --- Utility Functions ---
def preprocess_text(text):
    """Preprocess text for sentiment analysis"""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text.strip()

def validate_text_input(text_input):
    """Validate text input"""
    if not text_input or len(text_input.strip()) < 4:
        return False, 'Input too short. Please enter a meaningful sentence.'
    
    if not re.search('[a-zA-Z]', text_input):
        return False, 'Input must contain text.'
    
    return True, None

def predict_sentiment(text_input, pipeline):
    """Predict sentiment for given text"""
    # Validate input
    is_valid, error_msg = validate_text_input(text_input)
    if not is_valid:
        return {'error': error_msg}
    
    if pipeline is None:
        return {'error': 'Model not available'}
    
    try:
        # Preprocess text
        processed_text = preprocess_text(text_input)
        
        # Get prediction probabilities
        probs = pipeline.predict_proba([processed_text])[0]
        prob_positive = probs[1]
        
        # Determine label
        if 0.40 <= prob_positive <= 0.60:
            label = "Intermediate"
            confidence_score = prob_positive
        elif prob_positive > 0.60:
            label = "Positive"
            confidence_score = prob_positive
        else:
            label = "Negative"
            confidence_score = probs[0]
        
        return {
            'label': label,
            'confidence_score': confidence_score,
            'probabilities': {
                'positive': float(prob_positive),
                'negative': float(probs[0])
            }
        }
        
    except Exception as e:
        return {'error': f'Prediction failed: {str(e)}'}

# --- Main App ---
def main():
    # Load model
    pipeline = load_model()
    
    # Title and description
    st.title("🧠 Universal Sentiment Analyzer")
    st.markdown("**Analyze sentiment of any text with AI-powered accuracy**")
    
    if pipeline is None:
        st.error("⚠️ Model not loaded. Please check if sentiment_pipeline.pkl exists in the repository.")
        st.info("To use this app locally, run: `python model_trainer.py` to generate the model file.")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("📊 About")
        st.info("""
        This sentiment analyzer uses:
        - **TF-IDF Vectorization**
        - **Logistic Regression**
        - **Three-tier classification**: Positive, Negative, Intermediate
        """)
        
        st.header("🎯 Quick Examples")
        examples = [
            "This movie is absolutely amazing!",
            "The service was terrible and disappointing.",
            "It was okay, nothing special.",
            "I love this product so much!",
            "Not sure how I feel about this."
        ]
        
        for example in examples:
            if st.button(f"📝 {example[:30]}...", key=example):
                st.session_state.example_text = example
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["🔍 Single Analysis", "📊 Batch Analysis", "ℹ️ Model Info"])
    
    with tab1:
        st.header("🔍 Single Text Analysis")
        
        # Get text input
        text_input = st.text_area(
            "Enter text to analyze:",
            value=st.session_state.get('example_text', ''),
            height=100,
            placeholder="Type or paste your text here..."
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            analyze_btn = st.button("🚀 Analyze Sentiment", type="primary")
        
        if analyze_btn and text_input:
            with st.spinner("Analyzing sentiment..."):
                result = predict_sentiment(text_input, pipeline)
                
                if 'error' in result:
                    st.error(f"❌ {result['error']}")
                else:
                    # Display results
                    label = result['label']
                    confidence = result['confidence_score']
                    
                    # Color coding
                    if label == "Positive":
                        st.success(f"😊 **{label}** (Confidence: {confidence:.1%})")
                    elif label == "Negative":
                        st.error(f"😞 **{label}** (Confidence: {confidence:.1%})")
                    else:
                        st.warning(f"😐 **{label}** (Confidence: {confidence:.1%})")
                    
                    # Probability breakdown
                    st.subheader("📊 Probability Breakdown")
                    prob_data = result['probabilities']
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Positive", f"{prob_data['positive']:.1%}")
                    with col2:
                        st.metric("Negative", f"{prob_data['negative']:.1%}")
                    
                    # Progress bars
                    st.progress(prob_data['positive'], text="Positive")
                    st.progress(prob_data['negative'], text="Negative")
    
    with tab2:
        st.header("📊 Batch Text Analysis")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload a CSV file with a 'text' column:",
            type=['csv'],
            help="CSV file should have a column named 'text' containing the texts to analyze"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                
                if 'text' not in df.columns:
                    st.error("❌ CSV file must contain a 'text' column")
                else:
                    st.success(f"✅ Loaded {len(df)} texts from file")
                    
                    if st.button("🚀 Analyze All Texts"):
                        progress_bar = st.progress(0)
                        results = []
                        
                        for i, text in enumerate(df['text'].dropna()):
                            result = predict_sentiment(str(text), pipeline)
                            results.append(result)
                            progress_bar.progress((i + 1) / len(df))
                        
                        # Create results dataframe
                        results_df = pd.DataFrame(results)
                        df_combined = pd.concat([df, results_df], axis=1)
                        
                        # Display results
                        st.subheader("📊 Analysis Results")
                        st.dataframe(df_combined)
                        
                        # Summary statistics
                        if 'label' in results_df.columns:
                            sentiment_counts = results_df['label'].value_counts()
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.subheader("📈 Sentiment Distribution")
                                st.bar_chart(sentiment_counts)
                            
                            with col2:
                                st.subheader("📋 Summary")
                                for sentiment, count in sentiment_counts.items():
                                    percentage = (count / len(results_df)) * 100
                                    st.metric(sentiment, f"{count} ({percentage:.1f}%)")
                        
                        # Download results
                        csv = df_combined.to_csv(index=False)
                        st.download_button(
                            "📥 Download Results",
                            csv,
                            "sentiment_analysis_results.csv",
                            "text/csv"
                        )
            
            except Exception as e:
                st.error(f"❌ Error processing file: {e}")
    
    with tab3:
        st.header("ℹ️ Model Information")
        
        if pipeline is not None:
            st.success("✅ Model loaded successfully")
            
            # Model details
            st.subheader("🔧 Model Architecture")
            st.code("""
            Pipeline:
            1. TF-IDF Vectorizer (1-2 grams)
            2. Logistic Regression Classifier
            
            Features:
            - Text preprocessing (lowercase, HTML removal, punctuation removal)
            - TF-IDF feature extraction
            - Three-tier sentiment classification
            """)
            
            # Classification thresholds
            st.subheader("🎯 Classification Thresholds")
            st.info("""
            - **Positive**: Probability > 60%
            - **Intermediate**: Probability 40-60%
            - **Negative**: Probability < 40%
            """)
            
            # Training info
            st.subheader("📚 Training Data")
            st.info("""
            - **Dataset**: IMDB Movie Reviews (50K samples)
            - **Split**: 80% training, 20% testing
            - **Preprocessing**: Stratified sampling for balanced classes
            """)
        else:
            st.error("❌ Model not available")
    
    # Footer
    st.markdown("---")
    st.markdown("**Universal Sentiment Analyzer v2.0** | Built with Streamlit & Scikit-learn")

if __name__ == "__main__":
    main()