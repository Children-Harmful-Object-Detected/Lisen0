import streamlit as st
import cv2
import numpy as np
import torch
from ultralytics import YOLO
from collections import deque
from pathlib import Path

# --- Project-specific Imports (absolute for robustness) ---
# Assuming these modules are in interfaces/streamlit_app/modules
from interfaces.streamlit_app.modules.transformer import TransformerClassifier
from interfaces.streamlit_app.modules.info import extract_pose_vector, draw_pose_on_image, draw_box_on_image

class RealtimeVideoProcessor:
    def __init__(self, model_yolo_path: Path, model_tf_path: Path, conf_threshold: float = 0.5):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load the combined YOLO model (Lisen.pt)
        self.yolo_combined = YOLO(str(model_yolo_path))
        
        # Load Transformer model
        self.transformer = TransformerClassifier(input_dim=34, num_classes=3)
        self.transformer.load_state_dict(torch.load(str(model_tf_path), map_location=self.device))
        self.transformer.to(self.device)
        self.transformer.eval()

        self.conf_threshold = conf_threshold
        
        # Initialize buffer for pose sequences
        self.seq_buffer = deque(maxlen=12)
        
        # Risk classification labels and colors
        self.LABEL_MAP = ["Safety", "Warning", "Danger"]
        self.COLOR_MAP = [(0, 255, 0), (0, 255, 255), (0, 0, 255)] # Green, Yellow, Red

    def process_frame(self, frame: np.ndarray) -> dict:
        tf_label, tf_score = "Safety", 0.0
        
        # --- 1. Run combined YOLO model (Lisen.pt) ---
        results_combined = self.yolo_combined(frame, conf=self.conf_threshold, verbose=False)[0]
        
        # --- 2. Extract Pose Vector for Transformer ---
        if hasattr(results_combined, "keypoints") and results_combined.keypoints is not None:
            # st.write(f"Keypoints found: {len(results_combined.keypoints.data)}") # Debug line
            pose_vec = extract_pose_vector(results_combined)
        else:
            pose_vec = None
        
        # st.write(f"Pose Vec extracted: {pose_vec is not None}, Buffer len: {len(self.seq_buffer)}") # Debug line

        if pose_vec is not None:
            self.seq_buffer.append(pose_vec)

        # --- 3. Run Transformer if buffer is full ---
        if len(self.seq_buffer) == 12: # Full sequence length
            # st.write("Transformer buffer is full, running inference...") # Debug line
            seq = np.array(self.seq_buffer, dtype=np.float32)
            seq_tensor = torch.tensor(seq).unsqueeze(0).to(self.device)

            with torch.no_grad():
                out = self.transformer(seq_tensor)
                prob = torch.softmax(out, dim=1)[0].cpu().numpy()

            pred = int(np.argmax(prob))
            tf_label = self.LABEL_MAP[pred]
            tf_score = float(prob[pred])
            
        # --- 4. Danger Scoring and Reinforcement ---
        is_danger = False
        danger_score_from_transformer = tf_score if tf_label == "Danger" else 0.0
        danger_score_from_obj_det = 0.0

        for r_obj in results_combined.boxes: # Iterate through all detections from Lisen.pt
            cls_name = self.yolo_combined.names[int(r_obj.cls[0])].lower()
            conf = float(r_obj.conf[0])
            if cls_name == "violence": # If Lisen.pt detects violence, reinforce danger score
                danger_score_from_obj_det = max(danger_score_from_obj_det, conf)
        
        final_danger_score = max(danger_score_from_transformer, danger_score_from_obj_det)
        if tf_label == "Danger" or danger_score_from_obj_det > 0.5:
            is_danger = True
            
        # --- 5. Annotation ---
        annotated_frame = frame.copy()
        
        # Draw Pose (Adult/Child keypoints, no labels as per previous change)
        annotated_frame, pose_used_y = draw_pose_on_image(annotated_frame, results_combined, self.yolo_combined.names)
        
        # Draw Object Detection (Violence/Normal from Lisen.pt)
        # Pass the same results_combined, and draw_box_on_image will filter by name
        annotated_frame = draw_box_on_image(annotated_frame, results_combined, self.yolo_combined.names, pose_used_y)

        # Draw Transformer Risk Label
        tf_color = self.COLOR_MAP[self.LABEL_MAP.index(tf_label)]
        cv2.putText(annotated_frame, f"Risk: {tf_label} ({tf_score:.2f})",
                    (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1.0, tf_color, 3, cv2.LINE_AA)

        return {
            "annotated_frame": annotated_frame,
            "is_danger": is_danger,
            "danger_score": final_danger_score,
            "risk_label": tf_label,
            "risk_score_transformer": tf_score,
            "violence_score_obj_det": danger_score_from_obj_det
        }
