import torch
from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path

class YoloInferencer:
    def __init__(self, model_path: Path, conf_threshold: float = 0.5):
        # Ensure model_path is a string for YOLO constructor
        self.model = YOLO(str(model_path))
        self.conf_threshold = conf_threshold
        self.names = self.model.names # Class names from the model

    def infer_frame(self, frame: np.ndarray) -> dict:
        results = self.model(frame, conf=self.conf_threshold, verbose=False)
        annotated_frame = results[0].plot() # YOLO's built-in plotter

        is_danger = False
        danger_score = 0.0
        
        # Simple placeholder logic for danger based on object detection
        # This will need to be refined based on the actual project definition of "danger"
        # The user's 1_Realtime_Monitor.py implies this is returned by the inferencer.
        
        # Example: Accumulate confidence for 'Adult' detections. If it passes a threshold, consider it danger.
        # This assumes the YOLO model detects 'Adult' and 'Child' as its primary classes.
        # We need to know which class ID corresponds to 'Adult' or 'Child' if we want to make it more specific.
        # For now, let's assume class 0 is 'Adult' and class 1 is 'Child' (common for pose models).
        
        # More robust logic would involve fusion model or rule-based system.
        
        adult_conf = 0.0
        child_conf = 0.0

        for r in results[0].boxes:
            cls = int(r.cls[0])
            conf = float(r.conf[0])
            
            if self.names:
                if self.names[cls].lower() == 'adult':
                    adult_conf = max(adult_conf, conf)
                elif self.names[cls].lower() == 'child':
                    child_conf = max(child_conf, conf)

        # Placeholder danger logic:
        # If both adult and child are present, and adult confidence is high, consider it for risk calculation.
        # The actual 'danger' will likely come from a Transformer or a rule.
        # For a basic inferencer, let's use a very simplified rule:
        # if a child is detected, and there's interaction potentially.
        # Or, just return some score and `is_danger` will be set by external logic.
        
        # Based on 1_Realtime_Monitor.py, inferencer returns a danger score.
        # Let's make the danger score dependent on the detection confidence.
        # Assuming higher confidence detections contribute to a "score".
        
        if adult_conf > 0.3 and child_conf > 0.3: # Both detected implies potential interaction
            danger_score = adult_conf * child_conf # Simple interaction score
            if danger_score > 0.2: # Arbitrary threshold for initial danger flag
                is_danger = True
        
        # If no specific danger logic is provided in original, a basic score accumulation based on confidence is simple.
        
        return {
            "annotated_frame": annotated_frame,
            "is_danger": is_danger,
            "danger_score": danger_score,
            "adult_conf": adult_conf,
            "child_conf": child_conf
        }
