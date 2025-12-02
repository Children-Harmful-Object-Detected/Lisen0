import streamlit as st
from interfaces.streamlit_app.modules.action_labeler import run_action_labeler

def render_tab(DATA_RAW, DATA_PROC):
    """Renders the content for Tab 4: Action Labeling."""
    st.header("🎬 행동(Action) 라벨링")
    run_action_labeler(DATA_RAW, DATA_PROC)
