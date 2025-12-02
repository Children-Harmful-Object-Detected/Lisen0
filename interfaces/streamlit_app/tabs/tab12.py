import streamlit as st
from pathlib import Path
from ..modules.inference_v2 import show_inference_v2_tab

def render_tab(MODEL_DIR: Path, DATA_PROC: Path):
    """Renders the content for the V2 Inference Lab tab."""
    show_inference_v2_tab(MODEL_DIR, DATA_PROC)
