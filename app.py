import streamlit as st
import joblib
import inference_service
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

# --- Page Configuration ---
st.set_page_config(
    page_title="Universal Sentiment Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS (White/Dark Blue/Red Theme) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1A1A1A;
    }
    
    /* Backgrounds handled by config.toml (White) */
    
    /* Card/Container Styles */
    .css-1r6slb0, .css-12oz5g7, .stTab {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    /* Headers - Dark Blue */
    h1, h2, h3 {
        color: #002B5B !important;
        font-weight: 700;
    }
    
    /* Sidebar Overrides */
    [data-testid="stSidebar"] {
        background-color: #F8F9FA;
        border-right: 1px solid #E0E0E0;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 6px;
        color: #1A1A1A;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #002B5B !important;
        color: white !important;
        border-color: #002B5B !important;
    }

    /* Result Cards */
    .result-card-pos {
        background-color: #E8F5E9; /* Light Green */
        color: #1B5E20;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 6px solid #2E7D32; /* Strong Green */
        margin-top: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .result-card-neg {
        background-color: #FFEBEE; /* Light Red */
        color: #B71C1C;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 6px solid #D32F2F; /* Accent Red */
        margin-top: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .result-card-neu {
        background-color: #FFF3E0; /* Light Orange */
        color: #E65100;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 6px solid #EF6C00; /* Accent Orange */
        margin-top: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* History Item */
    .history-item {
        padding: 10px;
        margin-bottom: 8px;
        border-radius: 6px;
        font-size: 0.9rem;
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        color: #333;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    .history-pos { border-left: 4px solid #2E7D32; }
    .history-neg { border-left: 4px solid #D32F2F; }
    .history-neu { border-left: 4px solid #EF6C00; }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        background-color: #002B5B; /* Dark Blue Primary */
        color: white;
        border: none;
        padding: 0.6rem 1rem;
        transition: background 0.3s;
    }
    .stButton > button:hover {
        background-color: #001A38; /* Darker Blue */
        box-shadow: 0 4px 8px rgba(0, 43, 91, 0.2);
    }
    
    /* Input Text Area */
    .stTextArea textarea {
        border-radius: 8px;
        border: 1px solid #CCC;
        background-color: #FAFAFA;
    }
    .stTextArea textarea:focus {
        border-color: #002B5B;
        box-shadow: 0 0 0 1px #002B5B;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Session State ---
if 'review_text' not in st.session_state:
    st.session_state['review_text'] = ""
if 'history' not in st.session_state:
    st.session_state['history'] = []

def translate_and_analyze(text):
    """
    Helper to detect/translate text and run prediction.
    Returns: (result_dict, original_text, translated_text, src_lang)
    """
    try:
        # Simple heuristic: If it works, it works. 
        # Deep Translator's GoogleTranslator is robust.
        # We'll just translate to english. If it's already english, it stays roughly same.
        translator = GoogleTranslator(source='auto', target='en')
        translated = translator.translate(text)
        
        # We don't get 'src_lang' easily from deep_translator without another call or diff lib
        # So we'll just check if text differs significantly to guess if translation happened
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
with st.sidebar:
    st.markdown("## 🧠 Universal Analyzer")
    
    st.markdown("### 📜 Recent History")
    if not st.session_state['history']:
        st.info("No analysis yet.")
    else:
        for item in st.session_state['history'][:5]:
            if item['label'] == "Positive":
                color_class = "history-pos"
            elif item['label'] == "Intermediate":
                color_class = "history-neu"
            else:
                color_class = "history-neg"
                
            st.markdown(f"""
            <div class="history-item {color_class}">
                <b style="color:#002B5B">{item['label']}</b> ({item['conf']:.0%})<br>
                <i style="color:#888">{item['time']}</i><br>
                {item['text']}
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info("This AI analyzes text sentiment using **Logistic Regression** and **TF-IDF**. It is optimized for general English text.")

# --- Main Interface ---
st.title("Universal Sentiment Analyzer")
st.markdown("Analyze the emotional tone of **products**, **movies**, **services**, or **any text**.")

# TABS
# TABS
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🔮 Analyzer", "🔗 URL Analysis", "📂 Bulk Analysis", "⚔️ Compare", "📊 Data Insights", "🧠 Model Info"])

# ================= TAB 1: ANALYZER =================
with tab1:
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("### ✍️ Enter Text")
        
        # Generic Quick Examples
        st.markdown("Quick Examples:")
        c1, c2, c3 = st.columns(3)
        if c1.button("📱 Great Product", width="stretch"):
            set_text("I absolutely love this new phone! The camera is stunning and the battery lasts all day.")
        if c2.button("😡 Bad Service", width="stretch"):
            set_text("Terrible customer support. I waited on hold for an hour and they were rude.")
        if c3.button("💼 Professional", width="stretch"):
            set_text("The meeting went well, but there are some concerns about the timeline.")

        text_input = st.text_area(
            "Input Text",
            value=st.session_state['review_text'],
            height=200,
            placeholder="Type anything here... (e.g. 'This restaurant was amazing!')",
            key="main_input",
            label_visibility="collapsed"
        )
        analyze_btn = st.button("🚀 Analyze Sentiment", width="stretch")

    with col2:
        st.markdown("### 📊 Result")
        
        if analyze_btn:
            input_text = st.session_state.get('main_input')
            if input_text:
                try:
                    # UPDATED: Use Translation Layer
                    with st.spinner("Analyzing (and translating if needed)..."):
                        result, original, translated, is_translated = translate_and_analyze(input_text)
                    
                    if 'error' in result:
                        st.error(result['error'])
                    else:
                        label = result['label']
                        conf = result['confidence_score']
                        
                        add_to_history(original, label, conf)
                        
                        # Show Translation Info
                        if is_translated:
                            st.info(f"🌍 Translated to English: \"{translated}\"")

                        if label == "Positive":
                            st.markdown(f"""<div class="result-card-pos"><h2>😄 Positive</h2><p>This text conveys satisfaction or happiness.</p></div>""", unsafe_allow_html=True)
                            st.balloons()
                        elif label == "Intermediate":
                             st.markdown(f"""<div class="result-card-neu"><h2>😐 Intermediate</h2><p>This text is neutral or mixed. It doesn't lean strongly either way.</p></div>""", unsafe_allow_html=True)
                        else:
                            st.markdown(f"""<div class="result-card-neg"><h2>😞 Negative</h2><p>This text conveys dissatisfaction or frustration.</p></div>""", unsafe_allow_html=True)
                        
                        st.markdown("")
                        st.markdown(f"**Confidence Score:** `{conf:.2%}`")
                        st.progress(conf)
                        
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please enter some text to analyze.")
        else:
             st.info("Enter text and click Analyze.")

# ================= TAB 2: URL ANALYSIS =================
with tab2:
    st.header("🔗 URL Sentiment Analyzer")
    st.markdown("Analyze the sentiment of a blog post, article, or news page.")
    
    url_input = st.text_input("Enter URL:", placeholder="https://example.com/article")
    
    if st.button("🌐 Fetch & Analyze"):
        if url_input:
            with st.spinner("Fetching content..."):
                try:
                    # 1. Fetch
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                    response = requests.get(url_input, headers=headers, timeout=10)
                    response.raise_for_status()
                    
                    # 2. Parse
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Remove scripts and styles
                    for script in soup(["script", "style", "nav", "footer", "header"]):
                        script.decompose()
                        
                    # Get text
                    page_text = soup.get_text(separator=' ', strip=True)
                    
                    # Limit text length to avoid token limits or huge processing time (e.g., first 5000 chars)
                    truncated_text = page_text[:5000]
                    
                    if not truncated_text:
                        st.error("Could not find meaningful text on this page.")
                    else:
                        st.subheader("📄 Extracted Text (Snippet)")
                        st.caption(truncated_text[:500] + "...")
                        
                        # 3. Analyze
                        # We use the raw text directly (assuming English for URLs usually, or rely on our scraping)
                        # Optional: Use translate layer here too, but webpages are huge. Let's stick to direct.
                        res = inference_service.predict_sentiment(truncated_text)
                        
                        st.subheader("🧠 Analysis Result")
                        if 'error' in res:
                            st.error(res['error'])
                        else:
                            label = res['label']
                            conf = res['confidence_score']
                            
                            color = "green" if label == "Positive" else "red" if label == "Negative" else "orange"
                            st.markdown(f"## Verdict: :{color}[{label}]")
                            st.progress(conf)
                            st.markdown(f"**Confidence:** {conf:.1%}")
                            
                            if label == "Positive":
                                st.success("This page has generally positive content.")
                            elif label == "Negative":
                                st.error("This page has generally negative content.")
                            else:
                                st.warning("This page is neutral or mixed.")

                except Exception as e:
                    st.error(f"Error fetching URL: {e}")
        else:
            st.warning("Please enter a URL.")

# ================= TAB 3: BULK ANALYSIS =================
with tab3:
    st.header("📂 Bulk Sentiment Analysis")
    st.markdown("Upload a CSV file to analyze thousands of reviews at once.")
    
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"File uploaded successfully! ({len(df)} rows)")
            st.dataframe(df.head())
            
            # Column Selection
            text_col = st.selectbox("Select the column containing text/reviews:", df.columns)
            
            if st.button("🚀 Analyze All"):
                with st.spinner("Analyzing... This may take a moment."):
                    # Run predictions
                    results = []
                    probs = []
                    
                    progress_bar = st.progress(0)
                    for i, text in enumerate(df[text_col]):
                        res = inference_service.predict_sentiment(str(text))
                        if 'error' in res:
                            results.append("Error")
                            probs.append(0.0)
                        else:
                            results.append(res['label'])
                            probs.append(res['confidence_score'])
                        
                        if i % 100 == 0:
                            progress_bar.progress((i + 1) / len(df))
                    
                    progress_bar.progress(100)
                    
                    df['Sentiment'] = results
                    df['Confidence'] = probs
                    
                    st.success("Analysis Complete!")
                    
                    # 1. Data Preview
                    st.subheader("📝 Results Preview")
                    st.dataframe(df.head(10))
                    
                    # 2. Charts
                    st.subheader("📊 Visualizations")
                    c1, c2 = st.columns(2)
                    
                    with c1:
                        st.markdown("**Sentiment Distribution**")
                        sentiment_counts = df['Sentiment'].value_counts()
                        st.bar_chart(sentiment_counts, color="#002B5B")
                        
                    with c2:
                        st.markdown("**Confidence Distribution**")
                        st.line_chart(df['Confidence'], color="#D32F2F")

                    # 3. Word Clouds
                    st.subheader("☁️ Word Clouds")
                    st.markdown("Most frequent words in Positive vs Negative reviews.")
                    
                    wc_col1, wc_col2 = st.columns(2)
                    
                    # Helper to generate WC
                    def show_wordcloud(text_data, title, col):
                        if text_data:
                            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
                            fig, ax = plt.subplots(figsize=(10, 5))
                            ax.imshow(wordcloud, interpolation='bilinear')
                            ax.axis("off")
                            ax.set_title(title, fontsize=20, color='#002B5B')
                            col.pyplot(fig)
                            plt.close(fig) # Close to save memory
                        else:
                            col.info(f"No text data for {title}")

                    with wc_col1:
                        pos_text = " ".join(df[df['Sentiment'] == 'Positive'][text_col].dropna().astype(str))
                        show_wordcloud(pos_text, "Positive Words", wc_col1)
                        
                    with wc_col2:
                        neg_text = " ".join(df[df['Sentiment'] == 'Negative'][text_col].dropna().astype(str))
                        show_wordcloud(neg_text, "Negative Words", wc_col2)

                    # 4. Download
                    st.markdown("---")
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name='sentiment_analysis_results.csv',
                        mime='text/csv',
                    )
                    
        except Exception as e:
            st.error(f"Error processing file: {e}")

# ================= TAB 4: COMPARE =================
with tab4:
    st.header("⚔️ Compare Texts")
    st.markdown("Compare the sentiment of two different texts side-by-side.")
    
    comp_c1, comp_c2 = st.columns(2)
    
    with comp_c1:
        st.subheader("Text A")
        text_a = st.text_area("Enter Text A", height=150, placeholder="Type first text here...")
        
    with comp_c2:
        st.subheader("Text B")
        text_b = st.text_area("Enter Text B", height=150, placeholder="Type second text here...")
        
    if st.button("⚔️ Compare Now"):
        if text_a and text_b:
            res_a = inference_service.predict_sentiment(text_a)
            res_b = inference_service.predict_sentiment(text_b)
            
            # Display Result A
            with comp_c1:
                if 'error' in res_a:
                    st.error(res_a['error'])
                else:
                    label_a = res_a['label']
                    conf_a = res_a['confidence_score']
                    color = "green" if label_a == "Positive" else "red" if label_a == "Negative" else "orange"
                    st.markdown(f"**Valid Sentiment:** :{color}[{label_a}]")
                    st.progress(conf_a)
                    st.caption(f"Confidence: {conf_a:.1%}")

            # Display Result B
            with comp_c2:
                if 'error' in res_b:
                    st.error(res_b['error'])
                else:
                    label_b = res_b['label']
                    conf_b = res_b['confidence_score']
                    color = "green" if label_b == "Positive" else "red" if label_b == "Negative" else "orange"
                    st.markdown(f"**Valid Sentiment:** :{color}[{label_b}]")
                    st.progress(conf_b)
                    st.caption(f"Confidence: {conf_b:.1%}")
                    
            # Verdict
            st.markdown("---")
            st.subheader("🏆 Verdict")
            
            # Logic to determine "winner" (most positive)
            score_a = res_a.get('confidence_score', 0) if res_a.get('label') == 'Positive' else -res_a.get('confidence_score', 0)
            score_b = res_b.get('confidence_score', 0) if res_b.get('label') == 'Positive' else -res_b.get('confidence_score', 0)
            
            if res_a.get('label') == 'Intermediate': score_a = 0
            if res_b.get('label') == 'Intermediate': score_b = 0

            # Simple comparison logic (just for fun msg)
            if score_a > score_b:
                st.success("Text A is more Positive! 🌟")
            elif score_b > score_a:
                st.success("Text B is more Positive! 🌟")
            else:
                st.info("Both texts have similar sentiment.")
                
        else:
            st.warning("Please enter both texts.")

# ================= TAB 5: DATA INSIGHTS =================
with tab5:
    st.header("📊 Training Data (IMDB)")
    st.markdown("The model was trained on 50,000 movie reviews, but generalizes well to other English text.")
    
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        st.subheader("Class Balance")
        if os.path.exists("class_distribution.png"):
            st.image("class_distribution.png", caption="Positive vs Negative Split", width="stretch")
    with d_col2:
        st.subheader("Text Lengths")
        if os.path.exists("review_length.png"):
            st.image("review_length.png", caption="Character Counts", width="stretch")

# ================= TAB 3: MODEL INFO =================
# ================= TAB 6: MODEL INFO =================
with tab6:
    st.header("🧠 Model Architecture")
    
    if os.path.exists("model_metrics.pkl"):
        metrics = joblib.load("model_metrics.pkl")
        acc = metrics.get('accuracy', 0.0)
        
        st.metric("Baseline Accuracy", f"{acc:.2%}")
        st.markdown("### How it works")
        st.markdown("""
        1.  **Text Preprocessing**: Cleans text (lowercase, remove punctuation).
        2.  **TF-IDF**: Converts words into numbers based on frequency/rarity.
        3.  **Logistic Regression**: Calculates the probability of Positive/Negative.
        """)
    else:
        st.error("Model metrics unavailable.")
