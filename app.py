import streamlit as st
import joblib
import enhanced_inference_service as inference_service
import os
import re
import pandas as pd
from datetime import datetime
import requests

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
if "url_result" not in st.session_state:
    st.session_state["url_result"] = None
if "url_snippet" not in st.session_state:
    st.session_state["url_snippet"] = None
if "compare_result_a" not in st.session_state:
    st.session_state["compare_result_a"] = None
if "compare_result_b" not in st.session_state:
    st.session_state["compare_result_b"] = None


# --- Logic Helpers ---
def translate_and_analyze(text):
    res = inference_service.predict_sentiment(text)
    return res, text, text, False


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

# TABS
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "🔮 Analyzer",
        "🔗 URL Analysis",
        "📂 Bulk Analysis",
        "⚔️ Compare",
        "📊 Data Insights",
        "🧠 Model Info",
    ]
)

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
            set_text(
                "The meeting went well, but there are some concerns about timelines."
            )

        text_input = st.text_area(
            "Input Text",
            height=200,
            placeholder="Type anything here...",
            key="main_input",
            label_visibility="collapsed",
        )
        analyze_btn = st.button("🚀 Analyze Sentiment", use_container_width=True)

    with col2:
        st.markdown("### 📊 Result")

        if analyze_btn:
            input_text = st.session_state.get("main_input")
            if input_text:
                try:
                    with st.spinner("Analyzing..."):
                        (
                            result,
                            original,
                            translated,
                            is_translated,
                        ) = translate_and_analyze(input_text)

                    if "error" in result:
                        st.error(result["error"])
                    else:
                        label = result["label"]
                        conf = result["confidence_score"]

                        add_to_history(original, label, conf)

                        if is_translated:
                            st.info(f'🌍 Translated: "{translated}"')

                        ui.render_result_card(label, conf, translated)

                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please enter some text.")
        else:
            st.markdown(
                """
             <div class="glass-card" style="text-align: center; color: #888;">
                <p>Results will appear here...</p>
             </div>
             """,
                unsafe_allow_html=True,
            )

# ================= TAB 2: URL ANALYSIS =================
with tab2:
    st.header("🔗 URL Sentiment Analyzer")
    col1, col2 = st.columns([1.5, 1])

    with col1:
        url_input = st.text_input(
            "Enter URL:",
            placeholder="https://example.com/article",
            key="url_input_value",
        )
        if st.button("🌐 Fetch & Analyze", use_container_width=True):
            if url_input:
                with st.spinner("Fetching content..."):
                    try:
                        headers = {"User-Agent": "Mozilla/5.0"}
                        response = requests.get(url_input, headers=headers, timeout=10)
                        response.raise_for_status()
                        page_text = re.sub(r"<.*?>", " ", response.text)
                        page_text = re.sub(r"\s+", " ", page_text).strip()
                        truncated_text = page_text[:5000]

                        if not truncated_text:
                            st.error("Could not find meaningful text.")
                        else:
                            st.session_state["url_snippet"] = (
                                truncated_text[:500] + "..."
                            )
                            res = inference_service.predict_sentiment(truncated_text)
                            st.session_state["url_result"] = res
                    except Exception as e:
                        st.error(f"Error fetching URL: {e}")
                        st.session_state["url_result"] = None
                        st.session_state["url_snippet"] = None
            else:
                st.warning("Please enter a URL.")

        if st.session_state["url_snippet"]:
            st.subheader("📄 Extracted Snippet")
            st.code(st.session_state["url_snippet"])

    with col2:
        st.markdown("### 📊 Result")
        if st.session_state["url_result"]:
            res = st.session_state["url_result"]
            if "error" in res:
                st.error(res["error"])
            else:
                ui.render_result_card(
                    res["label"], res["confidence_score"], "URL Content"
                )
        else:
            st.markdown(
                """
             <div class="glass-card" style="text-align: center; color: #888;">
                <p>Results will appear here...</p>
             </div>
             """,
                unsafe_allow_html=True,
            )

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
                        if "error" in res:
                            results.append("Error")
                            probs.append(0.0)
                        else:
                            results.append(res["label"])
                            probs.append(res["confidence_score"])

                        if i % 50 == 0:
                            bar.progress((i + 1) / len(df))

                    bar.progress(100)
                    df["Sentiment"] = results
                    df["Confidence"] = probs

                    st.success("Done!")
                    st.dataframe(df.head(10), use_container_width=True)

                    # Visuals
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("**Sentiment Distribution**")
                        st.bar_chart(df["Sentiment"].value_counts())
                    with c2:
                        st.markdown("**Confidence Trend**")
                        st.line_chart(df["Confidence"])

                    # Download
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "📥 Download CSV", csv, "sentiment_results.csv", "text/csv"
                    )

        except Exception as e:
            st.error(f"Error: {e}")

# ================= TAB 4: COMPARE =================
with tab4:
    st.header("⚔️ Compare Texts")
    c1, c2 = st.columns(2)
    with c1:
        t_a = st.text_area(
            "Text A",
            height=150,
            placeholder="Type first text here...",
            key="compare_input_a",
        )
    with c2:
        t_b = st.text_area(
            "Text B",
            height=150,
            placeholder="Type second text here...",
            key="compare_input_b",
        )

    compare_btn = st.button("⚔️ Compare", use_container_width=True)

    if compare_btn:
        if t_a and t_b:
            with st.spinner("Comparing..."):
                st.session_state[
                    "compare_result_a"
                ] = inference_service.predict_sentiment(t_a)
                st.session_state[
                    "compare_result_b"
                ] = inference_service.predict_sentiment(t_b)
        else:
            st.warning("Please enter text in both fields.")

    if st.session_state["compare_result_a"] and st.session_state["compare_result_b"]:
        st.markdown("### 📊 Comparison Results")
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            r_a = st.session_state["compare_result_a"]
            if "error" in r_a:
                st.error(r_a["error"])
            else:
                ui.render_result_card(r_a["label"], r_a["confidence_score"], "")
        with res_col2:
            r_b = st.session_state["compare_result_b"]
            if "error" in r_b:
                st.error(r_b["error"])
            else:
                ui.render_result_card(r_b["label"], r_b["confidence_score"], "")

# ================= TAB 5: DATA INSIGHTS =================
with tab5:
    st.header("📊 Methods & Data Insights")
    d1, d2 = st.columns(2)
    with d1:
        st.subheader("⚖️ Training Data Balance")
        dist_df = pd.DataFrame(
            {"Count": [20000, 20000]}, index=["Negative", "Positive"]
        )
        st.bar_chart(dist_df, color="#6C5DD3")
        st.caption(
            "Distribution of positive and negative reviews in the IMDB training dataset (40,000 samples)."
        )
    with d2:
        st.subheader("📏 Average Review Length")
        len_df = pd.DataFrame(
            {"Average Length (Chars)": [1298, 1323]}, index=["Negative", "Positive"]
        )
        st.bar_chart(len_df, color="#FF754C")
        st.caption(
            "Average character count of negative vs. positive reviews in the dataset."
        )

# ================= TAB 6: MODEL INFO =================
with tab6:
    st.header("🧠 Model Architecture")
    st.markdown(
        """
    <div class="glass-card">
        <h3>Architecture</h3>
        <ul>
            <li><strong>Algorithm:</strong> Logistic Regression</li>
            <li><strong>Vectorization:</strong> TF-IDF (Term Frequency-Inverse Document Frequency)</li>
            <li><strong>Training Set:</strong> 50,000 IMDB Reviews</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if os.path.exists("model_metrics.pkl"):
        metrics = joblib.load("model_metrics.pkl")
        st.metric("Model Accuracy", f"{metrics.get('accuracy', 0.90):.2%}")
