import streamlit as st
import joblib
import inference_service
import os
import pandas as pd
from datetime import datetime

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
tab1, tab2, tab3 = st.tabs(["🔮 Analyzer", "📊 Data Insights", "🧠 Model Info"])

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
                    result = inference_service.predict_sentiment(input_text)
                    if 'error' in result:
                        st.error(result['error'])
                    else:
                        label = result['label']
                        conf = result['confidence_score']
                        
                        add_to_history(input_text, label, conf)
                        
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

# ================= TAB 2: DATA INSIGHTS =================
with tab2:
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
with tab3:
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
