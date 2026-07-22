import streamlit as st
from datetime import datetime


def render_sidebar():
    with st.sidebar:
        st.markdown("## 🧠 Universal Analyzer")

        st.markdown("### 📜 Recent History")
        if "history" not in st.session_state or not st.session_state["history"]:
            st.info("No analysis yet.")
        else:
            for item in st.session_state["history"][:5]:
                label_lower = item["label"].lower()
                if "positive" in label_lower:
                    lbl_cls = "hist-label-pos"
                elif "intermediate" in label_lower:
                    lbl_cls = "hist-label-neu"
                else:
                    lbl_cls = "hist-label-neg"

                st.markdown(
                    f"""
                <div class="history-item">
                    <span class="{lbl_cls}">{item['label']}</span> 
                    <span style="color:#4B5563; font-size:0.8em">({item['conf']:.0%})</span><br>
                    <i style="color:#6B7280; font-size:0.8em">{item['time']}</i><br>
                    <span style="color:#1F2937">{item['text']}</span>
                </div>
                """,
                    unsafe_allow_html=True,
                )

        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.info(
            "Sentiment Analysis v2.0\n\nOptimized for general English text using TF-IDF & Logistic Regression."
        )


def render_result_card(label, confidence, text):
    if label == "Positive":
        cls = "result-pos"
        icon = "😄"
        msg = "This text conveys satisfaction or happiness."
    elif label == "Intermediate":
        cls = "result-neu"
        icon = "😐"
        msg = "This text is neutral or mixed."
    else:
        cls = "result-neg"
        icon = "😞"
        msg = "This text conveys dissatisfaction or frustration."

    st.markdown(
        f"""
    <div class="result-card {cls}">
        <h2>{icon} {label}</h2>
        <p style="opacity: 0.9">{msg}</p>
        <div style="margin-top: 15px; background: rgba(0,0,0,0.05); padding: 10px; border-radius: 8px;">
            <small style="opacity: 0.8">CONFIDENCE SCORE</small><br>
            <strong style="font-size: 1.5em">{confidence:.1%}</strong>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
