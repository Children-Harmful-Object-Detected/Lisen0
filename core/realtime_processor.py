import streamlit as st
import cv2
import numpy as np
import torch
from ultralytics import YOLO
from collections import deque
from pathlib import Path

# --- Project-specific Imports (absolute for robustness) ---
<<<<<<< HEAD
=======
# Assuming these modules are in interfaces/streamlit_app/modules
>>>>>>> 7e1f10b3d9713a69b94b2694c8247664e7e86193
from interfaces.streamlit_app.modules.transformer import TransformerClassifier
from interfaces.streamlit_app.modules.info import extract_pose_vector, draw_pose_on_image, draw_box_on_image

class RealtimeVideoProcessor:
    def __init__(self, model_yolo_path: Path, model_tf_path: Path, conf_threshold: float = 0.5):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load the combined YOLO model (Lisen.pt)
<<<<<<< HEAD
        # Assuming Lisen.pt handles Pose + Violence/Non-Violence + Adult/Child
=======
>>>>>>> 7e1f10b3d9713a69b94b2694c8247664e7e86193
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
<<<<<<< HEAD
        # --- 1. Run combined YOLO model (Lisen.pt) ---
        # Run once, get both detection boxes and keypoints (if available)
        results_combined = self.yolo_combined(frame, conf=self.conf_threshold, verbose=False)[0]
        
        # YOLO Scores
        max_violence_conf = 0.0
        max_nonviolence_conf = 0.0
        
        for r_obj in results_combined.boxes:
            cls_name = self.yolo_combined.names[int(r_obj.cls[0])].lower()
            conf = float(r_obj.conf[0])
            
            # Check class names carefully
            if "non" in cls_name or "normal" in cls_name or "정상" in cls_name:
                max_nonviolence_conf = max(max_nonviolence_conf, conf)
            elif "violence" in cls_name or "폭력" in cls_name:
                max_violence_conf = max(max_violence_conf, conf)
            
        # --- 2. Extract Pose Vector for Transformer ---
        pose_vec = extract_pose_vector(results_combined) 
        
        if pose_vec is not None:
            self.seq_buffer.append(pose_vec)

        # Default values
        tf_label = "Safety"
        tf_score = 0.0
        viz_probs = [0.0, 0.0, 0.0]
        final_danger_score = 0.0

        # --- 3. Run Transformer if buffer is full ---
        if len(self.seq_buffer) == 12: # Full sequence length
            seq = np.array(self.seq_buffer, dtype=np.float32)
            seq_tensor = torch.tensor(seq).unsqueeze(0).to(self.device)
=======
        tf_label, tf_score = "Safety", 0.0
        
        # --- 1. Run combined YOLO model (Lisen.pt) ---
        results_combined = self.yolo_combined(frame, conf=self.conf_threshold, verbose=False)[0]
        
                    # --- 2. Extract Pose Vector for Transformer ---
                    # Assuming extract_pose_vector can handle combined results directly
                    pose_vec = extract_pose_vector(results_combined) 
                    
                    if pose_vec is not None:
                        self.seq_buffer.append(pose_vec)
        
                    # --- 3. Run Transformer if buffer is full ---
                    if len(self.seq_buffer) == 12: # Full sequence length
                        seq = np.array(self.seq_buffer, dtype=np.float32)            seq_tensor = torch.tensor(seq).unsqueeze(0).to(self.device)
>>>>>>> 7e1f10b3d9713a69b94b2694c8247664e7e86193

            with torch.no_grad():
                out = self.transformer(seq_tensor)
                prob = torch.softmax(out, dim=1)[0].cpu().numpy()

<<<<<<< HEAD
            # Raw Probabilities (Safety, Warning, Danger)
            viz_probs = prob.tolist() 
            
            # --- 4. Baseline Calculation (Pure Max Logic) ---
            # Use Transformer prediction directly for Label
            pred_idx = int(np.argmax(prob))
            tf_label = self.LABEL_MAP[pred_idx]
            tf_score = float(prob[pred_idx])
            
            # Final Danger Score is Max of YOLO Violence and TF Danger
            final_danger_score = max(viz_probs[2], max_violence_conf)

        # --- 5. Determine Final State Flags ---
        # Danger if TF says Danger OR YOLO says Violence > 0.5
        is_danger = (tf_label == "Danger") or (max_violence_conf > 0.5)
        
        # --- 6. Annotation ---
        annotated_frame = frame.copy()
        
        # Draw Pose (Skeleton) - Using Lisen.pt results
        annotated_frame, pose_used_y = draw_pose_on_image(annotated_frame, results_combined, self.yolo_combined.names)
        
        # Draw Box (Detection) - Using Lisen.pt results (Adult, Child, Violence, Non-Violence)
        annotated_frame = draw_box_on_image(annotated_frame, results_combined, self.yolo_combined.names, pose_used_y)

        # Draw Risk Label
        display_color = self.COLOR_MAP[self.LABEL_MAP.index(tf_label)]
        if is_danger: display_color = (0, 0, 255)
            
        cv2.putText(annotated_frame, f"Risk: {tf_label} ({tf_score:.2f})",
                    (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1.0, display_color, 2, cv2.LINE_AA)
=======
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
>>>>>>> 7e1f10b3d9713a69b94b2694c8247664e7e86193

        return {
            "annotated_frame": annotated_frame,
            "is_danger": is_danger,
            "danger_score": final_danger_score,
            "risk_label": tf_label,
            "risk_score_transformer": tf_score,
<<<<<<< HEAD
            "violence_score_obj_det": max_violence_conf,
            "nonviolence_score_obj_det": max_nonviolence_conf,
            "risk_probs": viz_probs
=======
            "violence_score_obj_det": danger_score_from_obj_det
>>>>>>> 7e1f10b3d9713a69b94b2694c8247664e7e86193
        }
