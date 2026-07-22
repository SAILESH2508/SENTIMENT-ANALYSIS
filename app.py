import streamlit as st
import joblib
import inference_service
import os
from datetime import datetime

# Custom Modules
import styles
import ui

# --- Page Configuration ---
st.set_page_config(
    page_title="Universal Sentiment Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Load CSS ---
st.markdown(styles.load_css(), unsafe_allow_html=True)

# --- Session State ---
if "main_input" not in st.session_state:
    st.session_state["main_input"] = ""
if "history" not in st.session_state:
    st.session_state["history"] = []


# --- Logic Helpers ---
def analyze_sentiment_text(text):
    res = inference_service.predict_sentiment(text)
    return res, text


def set_text(text):
    st.session_state["main_input"] = text


def add_to_history(text, label, confidence):
    st.session_state["history"].insert(
        0,
        {
            "time": datetime.now().strftime("%H:%M:%S"),
            "text": text[:50] + "..." if len(text) > 50 else text,
            "label": label,
            "conf": confidence,
        },
    )


# --- Sidebar ---
ui.render_sidebar()

# --- Main Interface ---
st.title("Universal Sentiment Analyzer")
st.markdown(
    "Analyze the emotional tone of **products**, **movies**, **services**, or **any text**."
)

col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown("### ✍️ Enter Text")

    # Quick Sample Examples
    st.markdown("Or try one of these quick examples:")
    c1, c2, c3 = st.columns(3)
    if c1.button("📱 Great Product", key="ex1"):
        set_text(
            "I absolutely love this new phone! The camera and battery life are stunning."
        )
    if c2.button("😡 Bad Service", key="ex2"):
        set_text(
            "Terrible customer support. I waited on hold for an hour and got no help."
        )
    if c3.button("💼 Professional", key="ex3"):
        set_text(
            "The quarterly project review went as expected with reasonable progress."
        )

    text_input = st.text_area(
        "Input Text",
        height=200,
        placeholder="Type or paste your text here to analyze sentiment...",
        key="main_input",
        label_visibility="collapsed",
    )
    analyze_btn = st.button("🚀 Analyze Sentiment", use_container_width=True)

with col2:
    st.markdown("### 📊 Analysis Result")

    if analyze_btn:
        input_text = st.session_state.get("main_input")
        if input_text:
            try:
                with st.spinner("Analyzing text sentiment..."):
                    result, original = analyze_sentiment_text(input_text)

                if "error" in result:
                    st.error(result["error"])
                else:
                    label = result["label"]
                    conf = result["confidence_score"]
                    add_to_history(original, label, conf)
                    ui.render_result_card(label, conf, original)

            except Exception as e:
                st.error(f"Error analyzing text: {e}")
        else:
            st.warning("Please enter some text before analyzing.")
    else:
        st.markdown(
            """
            <div class="glass-card" style="text-align: center; color: #888;">
                <p style="font-size: 1.1em;">👈 Enter text or select an example on the left, then click <strong>Analyze Sentiment</strong>.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Model Status Footer Card
st.markdown("---")
st.markdown("### 🧠 Model Overview")
st.markdown(
    """
    <div class="glass-card">
        <p><strong>Architecture:</strong> TF-IDF (Term Frequency - Inverse Document Frequency) + Logistic Regression Classifier</p>
        <p><strong>Dataset:</strong> 50,000 IMDB Movie Reviews (Balanced Sentiment Corpus)</p>
        <p><strong>Deployment:</strong> Containerized Docker & Jenkins Automated CI/CD Pipeline</p>
    </div>
    """,
    unsafe_allow_html=True,
)
