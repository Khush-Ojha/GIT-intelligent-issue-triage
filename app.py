# app.py

import streamlit as st
from predictor import predict_probabilities
import pandas as pd
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="G.I.T.S. - GitHub Issue Triage System",
    page_icon="🤖",
    layout="wide"
)

# --- NEW CUSTOM CSS FOR ANIMATED GRID BACKGROUND ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    .stApp {
        background-color: #0E1117;
        background-image: 
            linear-gradient(rgba(0, 191, 255, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 191, 255, 0.1) 1px, transparent 1px);
        background-size: 30px 30px;
        animation: pan 60s linear infinite;
        font-family: 'Inter', sans-serif;
    }

    @keyframes pan {
        0% { background-position: 0 0; }
        100% { background-position: 300px 300px; }
    }

    /* Polished, Modern Title */
    .stTitle {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 3em;
        color: #FFFFFF;
        padding-bottom: 20px;
    }
    
    /* Subheader styling */
    .stSubheader {
        color: #a0a0a0;
        font-family: 'Inter', sans-serif;
    }

    /* Styling for the containers to make them pop */
    .st-emotion-cache-1r4qj8v {
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 25px;
        background-color: rgba(14, 17, 23, 0.8); /* Slightly transparent background */
        backdrop-filter: blur(5px); /* Frosted glass effect */
    }
</style>
""", unsafe_allow_html=True)


# --- Session State Initialization ---
if 'analysis_triggered' not in st.session_state:
    st.session_state.analysis_triggered = False
if 'issue_title' not in st.session_state:
    st.session_state.issue_title = ""
if 'issue_body' not in st.session_state:
    st.session_state.issue_body = ""

def trigger_analysis():
    st.session_state.issue_title = st.session_state.widget_title
    st.session_state.issue_body = st.session_state.widget_body
    st.session_state.analysis_triggered = True

def reset_state():
    st.session_state.analysis_triggered = False
    st.session_state.issue_title = ""
    st.session_state.issue_body = ""


# --- Main App Logic ---
if not st.session_state.analysis_triggered:
    st.markdown('<h1 class="stTitle" style="text-align: center;">G.I.T.S.</h1>', unsafe_allow_html=True)
    st.markdown('<p class="stSubheader" style="text-align: center;">GitHub Issue Triage System - AI Assistant Online</p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div style="display: flex; justify-content: center;"> <div style="width: 60%;">', unsafe_allow_html=True)
        st.text_input("Subject Line (Title)", placeholder="e.g., Login button not working on Safari", key="widget_title")
        st.text_area("Full Report (Body)", placeholder="Describe anomaly in detail...", height=250, key="widget_body")
        st.button("Analyze & Triage", on_click=trigger_analysis, type="primary")
        st.markdown('</div></div>', unsafe_allow_html=True)
else:
    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        st.markdown('<h1 class="stTitle" style="font-size: 2em;">G.I.T.S.</h1>', unsafe_allow_html=True)
        st.markdown('<p class="stSubheader">Issue Transmission</p>', unsafe_allow_html=True)
        st.text_input("Subject Line (Title)", value=st.session_state.issue_title, disabled=True)
        st.text_area("Full Report (Body)", value=st.session_state.issue_body, height=300, disabled=True)
        st.button("Reset", on_click=reset_state)
    with col2:
        st.subheader("Analysis Output")
        if st.session_state.issue_title and st.session_state.issue_body:
            with st.spinner("...AI core processing..."):
                full_text = f"[TITLE]: {st.session_state.issue_title} [BODY]: {st.session_state.issue_body}"
                probabilities = predict_probabilities(full_text)
                df_probs = pd.DataFrame(list(probabilities.items()), columns=['Label', 'Confidence'])
                df_probs.sort_values(by='Confidence', ascending=False, inplace=True)
                best_guess = df_probs.iloc[0]

                st.write("Confidence Analysis:")
                st.bar_chart(df_probs.set_index('Label'))
                st.markdown("---")
                verdict_text = f"**AI Verdict:** `{best_guess['Label'].upper()}`\n\n**Confidence:** `{best_guess['Confidence']:.2%}`"
                st.markdown(verdict_text)
        else:
            # This part should ideally not be reached due to the state logic
            st.warning("Awaiting valid input.")