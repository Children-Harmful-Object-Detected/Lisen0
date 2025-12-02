import streamlit as st
import cv2
import numpy as np
import torch
from ultralytics import YOLO
from collections import deque
import av

from interfaces.streamlit_app.modules.transformer import TransformerClassifier
from interfaces.streamlit_app.modules.info import extract_pose_vector, draw_pose_on_image, draw_box_on_image


class VideoProcessor:
    def __init__(self, model_dir):
        self.model_dir = model_dir
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load models once
        self.yolo_pose = YOLO(str(self.model_dir / "best.pt"))
        self.yolo_box = YOLO(str(self.model_dir / "best.pt"))
        
        transformer_model_path = self.model_dir / "transformer_action_risk.pt"
        self.transformer = TransformerClassifier(input_dim=34, num_classes=3)
        self.transformer.load_state_dict(torch.load(transformer_model_path, map_location=self.device))
        self.transformer.to(self.device)
        self.transformer.eval()

        # Initialize buffer and risk state
        self.seq_buffer = deque(maxlen=12)
        self.tf_label = "Safety"
        self.tf_score = 0.0
        
        self.LABEL_MAP = ["Safety", "Warning", "Danger"]
        self.COLOR_MAP = [(0, 255, 0), (0, 255, 255), (0, 0, 255)]


    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")

        # --- Inference ---
        # 1. YOLO Pose
        r_pose = self.yolo_pose(img, conf=0.7, verbose=False)[0]
        
        # 2. YOLO Box (run separately for box-specific logic if any)
        r_box = self.yolo_box(img, conf=0.5, verbose=False)[0]

        # 3. Transformer
        pose_vec = extract_pose_vector(r_pose)
        if pose_vec is not None:
            self.seq_buffer.append(pose_vec)

        if len(self.seq_buffer) >= 12:
            seq = np.array(self.seq_buffer, dtype=np.float32)
            seq_tensor = torch.tensor(seq).unsqueeze(0).to(self.device)

            with torch.no_grad():
                out = self.transformer(seq_tensor)
                prob = torch.softmax(out, dim=1)[0].cpu().numpy()

            pred = int(np.argmax(prob))
            self.tf_label = self.LABEL_MAP[pred]
            self.tf_score = float(prob[pred])

        # --- Drawing ---
        # Draw pose and get used y-coordinates for labels to avoid overlap
        img, pose_used_y = draw_pose_on_image(img, r_pose, self.yolo_pose.names)
        
        # Draw boxes using the function that supports Korean labels
        img = draw_box_on_image(img, r_box, self.yolo_box.names, pose_used_y)

        # Draw risk status on the final frame
        tf_color = self.COLOR_MAP[self.LABEL_MAP.index(self.tf_label)]
        cv2.putText(img, f"{self.tf_label} {self.tf_score:.2f}",
                    (10, 35), cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, tf_color, 3, cv2.LINE_AA)

        return av.VideoFrame.from_ndarray(img, format="bgr24")
