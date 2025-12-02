import streamlit as st
from interfaces.streamlit_app.modules.training_tools import yolo_pose_training_tab

def render_tab(DATA_PROC, MODEL_DIR, RESULTS_DIR):
    """Renders the content for Tab 3: YOLO Pose Model Training."""
    st.header("🧠 Adult/Child 모델 학습")
    yolo_pose_training_tab(DATA_PROC, MODEL_DIR, RESULTS_DIR)
