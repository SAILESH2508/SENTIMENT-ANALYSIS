import streamlit as st
import joblib
import enhanced_inference_service as inference_service
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

# Custom Modules
import styles
import ui

# --- Page Configuration ---
st.set_page_config(
    page_title="Universal Sentiment Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load CSS ---
st.markdown(styles.load_css(), unsafe_allow_html=True)

# --- Session State ---
if 'review_text' not in st.session_state:
    st.session_state['review_text'] = ""
if 'history' not in st.session_state:
    st.session_state['history'] = []

# --- Logic Helpers ---
def translate_and_analyze(text):
    try:
        translator = GoogleTranslator(source='auto', target='en')
        translated = translator.translate(text)
        is_translated = (text.strip().lower() != translated.strip().lower())
        res = inference_service.predict_sentiment(translated)
        return res, text, translated, is_translated
    except Exception as e:
        return {'error': f"Translation/Analysis Error: {e}"}, text, text, False

def set_text(text):
    st.session_state['review_text'] = text

def add_to_history(text, label, confidence):
    st.session_state['history'].insert(0, {
        'time': datetime.now().strftime("%H:%M:%S"),
        'text': text[:50] + "..." if len(text) > 50 else text,
        'label': label,
        'conf': confidence
    })

# --- Sidebar ---
ui.render_sidebar()

# --- Main Interface ---
st.title("Universal Sentiment Analyzer")
st.markdown("Analyze the emotional tone of **products**, **movies**, **services**, or **any text**.")

# TABS
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔮 Analyzer", 
    "🔗 URL Analysis", 
    "📂 Bulk Analysis", 
    "⚔️ Compare", 
    "📊 Data Insights", 
    "🧠 Model Info"
])

# ================= TAB 1: ANALYZER =================
with tab1:
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("### ✍️ Enter Text")
        
        # Examples
        st.markdown("Or try one of these:")
        c1, c2, c3 = st.columns(3)
        if c1.button("📱 Great Product", key="ex1"):
            set_text("I absolutely love this new phone! The camera is stunning.")
        if c2.button("😡 Bad Service", key="ex2"):
            set_text("Terrible customer support. I waited on hold for an hour.")
        if c3.button("💼 Professional", key="ex3"):
            set_text("The meeting went well, but there are some concerns about timelines.")

        text_input = st.text_area(
            "Input Text",
            value=st.session_state['review_text'],
            height=200,
            placeholder="Type anything here...",
            key="main_input",
            label_visibility="collapsed"
        )
        analyze_btn = st.button("🚀 Analyze Sentiment", use_container_width=True)

    with col2:
        st.markdown("### 📊 Result")
        
        if analyze_btn:
            input_text = st.session_state.get('main_input')
            if input_text:
                try:
                    with st.spinner("Analyzing..."):
                        result, original, translated, is_translated = translate_and_analyze(input_text)
                    
                    if 'error' in result:
                        st.error(result['error'])
                    else:
                        label = result['label']
                        conf = result['confidence_score']
                        
                        add_to_history(original, label, conf)
                        
                        if is_translated:
                            st.info(f"🌍 Translated: \"{translated}\"")

                        ui.render_result_card(label, conf, translated)
                        
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please enter some text.")
        else:
             st.markdown("""
             <div class="glass-card" style="text-align: center; color: #888;">
                <p>Results will appear here...</p>
             </div>
             """, unsafe_allow_html=True)

# ================= TAB 2: URL ANALYSIS =================
with tab2:
    st.header("🔗 URL Sentiment Analyzer")
    url_input = st.text_input("Enter URL:", placeholder="https://example.com/article")
    
    if st.button("🌐 Fetch & Analyze"):
        if url_input:
            with st.spinner("Fetching content..."):
                try:
                    headers = {'User-Agent': 'Mozilla/5.0'}
                    response = requests.get(url_input, headers=headers, timeout=10)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Cleanup
                    for s in soup(["script", "style", "nav", "footer", "header"]):
                        s.decompose()
                        
                    page_text = soup.get_text(separator=' ', strip=True)
                    truncated_text = page_text[:5000]
                    
                    if not truncated_text:
                        st.error("Could not find meaningful text.")
                    else:
                        st.subheader("📄 Extracted Snippet")
                        st.code(truncated_text[:500] + "...")
                        
                        res = inference_service.predict_sentiment(truncated_text)
                        if 'error' in res:
                            st.error(res['error'])
                        else:
                            ui.render_result_card(res['label'], res['confidence_score'], "URL Content")

                except Exception as e:
                    st.error(f"Error fetching URL: {e}")

# ================= TAB 3: BULK ANALYSIS =================
with tab3:
    st.header("📂 Bulk Sentiment Analysis")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"Loaded {len(df)} rows")
            st.dataframe(df.head(), use_container_width=True)
            
            text_col = st.selectbox("Select text column:", df.columns)
            
            if st.button("🚀 Analyze All"):
                with st.spinner("Processing..."):
                    results, probs = [], []
                    bar = st.progress(0)
                    
                    for i, text in enumerate(df[text_col]):
                        res = inference_service.predict_sentiment(str(text))
                        if 'error' in res:
                            results.append("Error")
                            probs.append(0.0)
                        else:
                            results.append(res['label'])
                            probs.append(res['confidence_score'])
                        
                        if i % 50 == 0:
                            bar.progress((i + 1) / len(df))
                    
                    bar.progress(100)
                    df['Sentiment'] = results
                    df['Confidence'] = probs
                    
                    st.success("Done!")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    # Visuals
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("**Sentiment Distribution**")
                        st.bar_chart(df['Sentiment'].value_counts())
                    with c2:
                        st.markdown("**Confidence Trend**")
                        st.line_chart(df['Confidence'])

                    # Download
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Download CSV", csv, "sentiment_results.csv", "text/csv")
                    
        except Exception as e:
            st.error(f"Error: {e}")

# ================= TAB 4: COMPARE =================
with tab4:
    st.header("⚔️ Compare Texts")
    c1, c2 = st.columns(2)
    with c1:
        t_a = st.text_area("Text A", height=150)
    with c2:
        t_b = st.text_area("Text B", height=150)
        
    if st.button("⚔️ Compare"):
        if t_a and t_b:
            r_a = inference_service.predict_sentiment(t_a)
            r_b = inference_service.predict_sentiment(t_b)
            
            with c1:
                if 'error' not in r_a:
                    ui.render_result_card(r_a['label'], r_a['confidence_score'], "")
            with c2:
                if 'error' not in r_b:
                    ui.render_result_card(r_b['label'], r_b['confidence_score'], "")
        else:
            st.warning("Enter both texts.")

# ================= TAB 5: DATA INSIGHTS =================
with tab5:
    st.header("📊 Methods & Data")
    d1, d2 = st.columns(2)
    with d1:
        if os.path.exists("class_distribution.png"):
            st.image("class_distribution.png", caption="Training Data Balance")
        else:
            st.info("Class distribution image not found.")
    with d2:
        if os.path.exists("review_length.png"):
            st.image("review_length.png", caption="Review Lengths")
        else:
            st.info("Review length image not found.")

# ================= TAB 6: MODEL INFO =================
with tab6:
    st.header("🧠 Model Architecture")
    st.markdown("""
    <div class="glass-card">
        <h3>Architecture</h3>
        <ul>
            <li><strong>Algorithm:</strong> Logistic Regression</li>
            <li><strong>Vectorization:</strong> TF-IDF (Term Frequency-Inverse Document Frequency)</li>
            <li><strong>Training Set:</strong> 50,000 IMDB Reviews</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if os.path.exists("model_metrics.pkl"):
        metrics = joblib.load("model_metrics.pkl")
        st.metric("Model Accessibility", f"{metrics.get('accuracy', 0.90):.2%}")
