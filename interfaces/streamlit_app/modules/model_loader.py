import streamlit as st
import torch
from ultralytics import YOLO
from pathlib import Path
<<<<<<< HEAD
import yaml # Import yaml
=======
>>>>>>> 7e1f10b3d9713a69b94b2694c8247664e7e86193

from interfaces.streamlit_app.modules.transformer import TransformerClassifier

# Define device globally within this module
device = "cuda" if torch.cuda.is_available() else "cpu" 

@st.cache_resource
<<<<<<< HEAD
def load_models(config_path: Path): # Changed to take config_path
    # Load config file
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Get model paths from config
    yolo_model_path = Path(config['paths']['models']['yolo_champion'])
    transformer_model_path = Path(config['paths']['models']['transformer_judge'])

    # Load YOLO model
    yolo_pose = YOLO(str(yolo_model_path))
    yolo_box = YOLO(str(yolo_model_path)) # Both use the single Lisen.pt model

    # Instantiate Transformer model with correct parameters
    # input_dim=34 (from our data prep), num_classes=3 (Safety/Warning/Danger)
    transformer = TransformerClassifier(input_dim=34, num_classes=3) # num_layers will default to 3 now
    
    # Load Transformer state_dict
    transformer.load_state_dict(torch.load(transformer_model_path, map_location=device))
=======
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
>>>>>>> 7e1f10b3d9713a69b94b2694c8247664e7e86193
    transformer.to(device)
    transformer.eval()

    return yolo_pose, yolo_box, transformer
