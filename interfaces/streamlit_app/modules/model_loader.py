import streamlit as st
import torch
from ultralytics import YOLO
from pathlib import Path

from interfaces.streamlit_app.modules.transformer import TransformerClassifier

# Define device globally within this module
device = "cuda" if torch.cuda.is_available() else "cpu" 

@st.cache_resource
def load_models(MODEL_YOLO):
    yolo_pose = YOLO(str(MODEL_YOLO))
    yolo_box = YOLO(str(MODEL_YOLO)) # Both use the single Lisen.pt model
    transformer = TransformerClassifier(input_dim=34, num_classes=3)

    model_path = (
        Path("models/transformer_action_pose.pt")
        if Path("models/transformer_action_pose.pt").exists()
        else Path("models/transformer_action_risk.pt")
    )

    transformer.load_state_dict(torch.load(model_path, map_location=device))
    transformer.to(device)
    transformer.eval()

    return yolo_pose, yolo_box, transformer
