import streamlit as st
from interfaces.streamlit_app.modules.info import show_model_inference_tab, show_frame_labeling_tab

def render_tab(MODEL_YOLO, MODEL_DIR, DATA_PROC):
    """Renders the content for Tab 8: Model Inference and Frame Labeling."""
    selected_video = show_model_inference_tab(MODEL_YOLO, MODEL_DIR, DATA_PROC)
    if selected_video:
        show_frame_labeling_tab(MODEL_YOLO, selected_video)
