import streamlit as st
import cv2
import tempfile
import numpy as np
from pathlib import Path
import sys
import time

# --- Project-specific Imports ---
# Use absolute imports from project root (Lisen - 복사본)
from core.utils import load_config, resolve_path
from core.realtime_processor import RealtimeVideoProcessor # Changed from YoloInferencer

# Determine PROJECT_ROOT relative to this page file
PAGE_FILE_PATH = Path(__file__).resolve()
STREAMLIT_APP_DIR = PAGE_FILE_PATH.parent.parent # interfaces/streamlit_app
INTERFACES_DIR = STREAMLIT_APP_DIR.parent # interfaces
PROJECT_ROOT = INTERFACES_DIR.parent # Lisen - 복사본

# Config Path is at PROJECT_ROOT / "config.yaml"
CONFIG_PATH = PROJECT_ROOT / "config.yaml"

# Load Config
try:
    config = load_config(str(CONFIG_PATH))
except Exception as e:
    st.error(f"❌ 설정 파일 로드 실패: {e}")
    st.stop()

# Resolve Model Paths from config
MODEL_YOLO_PATH = resolve_path(str(CONFIG_PATH), config['paths']['models']['yolo_champion'])
MODEL_TF_PATH = resolve_path(str(CONFIG_PATH), config['paths']['models']['transformer_judge'])


def app(): # Renamed main() to app() for Streamlit multi-page app convention
    st.set_page_config(page_title="Real-time Monitor", page_icon="📹", layout="wide")
    st.title("📹 Real-time Intelligence Monitor")
    
    # Sidebar Options
    st.sidebar.header("Monitor Settings")
    
    st.sidebar.text(f"Combined YOLO Model: {MODEL_YOLO_PATH.name}")
    st.sidebar.text(f"Transformer Model: {MODEL_TF_PATH.name}")
    
    conf_thres = st.sidebar.slider("Confidence Threshold", 0.1, 0.9, 0.5, 0.05, key="conf_thres_rtm")
    stride = st.sidebar.slider("프레임 간격 (Stride)", 1, 15, 1, key="frame_stride_rtm") # New stride setting
    
    # Input Source
    input_source = st.sidebar.radio("Input Source", ["Upload Video", "Webcam"], key="input_source_rtm")

    # --- Start Frame Setting for Upload Video ---
    start_frame = 0
    if input_source == "Upload Video":
        st.sidebar.markdown("---")
        st.sidebar.subheader("Video Analysis Start Point")
        
        # Initialize session state for dynamic start_frame control
        if "current_start_frame_rtm" not in st.session_state:
            st.session_state.current_start_frame_rtm = 0
            
        start_frame_input = st.sidebar.number_input("시작 프레임 (Start Frame)", min_value=0, value=st.session_state.current_start_frame_rtm, step=10, key="start_frame_input_rtm")
        st.session_state.current_start_frame_rtm = start_frame_input # Keep session state in sync
        start_frame = start_frame_input # Use this for video processing
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("Frame Navigation")
        
        col_prev, col_next = st.sidebar.columns(2)
        
        with col_prev:
            if st.button("-100 Frames", key="prev_100_rtm"):
                st.session_state.current_start_frame_rtm = max(0, st.session_state.current_start_frame_rtm - 100)
                st.rerun()
            if st.button("-50 Frames", key="prev_50_rtm"):
                st.session_state.current_start_frame_rtm = max(0, st.session_state.current_start_frame_rtm - 50)
                st.rerun()
            if st.button("-10 Frames", key="prev_10_rtm"):
                st.session_state.current_start_frame_rtm = max(0, st.session_state.current_start_frame_rtm - 10)
                st.rerun()
        
        with col_next:
            if st.button("+10 Frames", key="next_10_rtm"):
                st.session_state.current_start_frame_rtm += 10
                st.rerun()
            if st.button("+50 Frames", key="next_50_rtm"):
                st.session_state.current_start_frame_rtm += 50
                st.rerun()
            if st.button("+100 Frames", key="next_100_rtm"):
                st.session_state.current_start_frame_rtm += 100
                st.rerun()
    # Initialize RealtimeVideoProcessor
    @st.cache_resource
    def get_realtime_processor(yolo_path, tf_path, conf):
        return RealtimeVideoProcessor(yolo_path, tf_path, conf)

    try:
        processor = get_realtime_processor(MODEL_YOLO_PATH, MODEL_TF_PATH, conf_thres)
        processor.conf_threshold = conf_thres # Dynamic update of threshold
    except Exception as e:
        st.error(f"❌ 모델 로드 오류: {e}")
        st.stop()

    # Main Display Area
    col_video, col_stats = st.columns([3, 1])

    with col_stats:
        st.subheader("Live Stats")
        status_indicator = st.empty()
        score_gauge = st.empty()
        alert_box = st.empty()

    with col_video:
        stframe = st.empty()
        
        if input_source == "Upload Video":
            uploaded_file = st.file_uploader("Choose a video file...", type=["mp4", "avi", "mov"], key="uploaded_file_rtm")
            
            if uploaded_file is not None:
                # Save uploaded file to temp
                tfile = tempfile.NamedTemporaryFile(delete=False) 
                tfile.write(uploaded_file.read())
                
                vf = cv2.VideoCapture(tfile.name)
                total_frames = int(vf.get(cv2.CAP_PROP_FRAME_COUNT))
                
                # Adjust start_frame if it exceeds total_frames
                if start_frame >= total_frames:
                    start_frame = total_frames - 1
                    st.sidebar.warning(f"시작 프레임이 총 프레임({total_frames})을 초과하여 {start_frame}으로 조정됩니다.")

                st.sidebar.info(f"선택 영상 총 프레임: {total_frames}")
                st.sidebar.number_input("조정된 시작 프레임", value=start_frame, disabled=True, key="display_start_frame_rtm")


                start_button = st.button("▶ Start Analysis", key="start_rtm")
                stop_button = st.button("⏹ Stop", key="stop_rtm")
                
                if "stop_analysis_rtm" not in st.session_state:
                    st.session_state.stop_analysis_rtm = False

                if stop_button:
                    st.session_state.stop_analysis_rtm = True
                if start_button:
                    st.session_state.stop_analysis_rtm = False 

                if start_button and not st.session_state.stop_analysis_rtm:
                    st.write(f"DEBUG: Attempting to set start frame to: {start_frame}")
                    set_pos_success = vf.set(cv2.CAP_PROP_POS_FRAMES, start_frame) # Set video start position
                    st.write(f"DEBUG: vf.set(CAP_PROP_POS_FRAMES, {start_frame}) returned: {set_pos_success}")
                    st.write(f"DEBUG: Actual frame position after set: {vf.get(cv2.CAP_PROP_POS_FRAMES)}")

                    frame_count = start_frame # Initialize frame counter with start_frame
                    st.write(f"DEBUG: Initial frame_count for loop: {frame_count}")
                    while vf.isOpened() and not st.session_state.stop_analysis_rtm:
                        ret, frame = vf.read()
                        if not ret:
                            break

                        if frame_count % stride == 0: # Apply stride
                            result = processor.process_frame(frame) # Changed from inferencer.infer_frame
                            
                            stframe.image(result["annotated_frame"], channels="BGR")
                            
                            if result["is_danger"]:
                                status_indicator.error("⚠️ DANGER DETECTED")
                                alert_box.markdown("🚨 **Violence / Abuse Detected!**")
                            else:
                                status_indicator.success("✅ Normal")
                                alert_box.empty()
                                
                            score_gauge.metric("Danger Score", f"{result['danger_score']:.2f}")
                        frame_count += 1 # Increment frame count regardless of stride
                            
                    vf.release()
                    st.success("Analysis Complete.")

        elif input_source == "Webcam":
            st.info("웹캠 지원은 로컬 머신에서 카메라 접근 권한이 필요합니다.")
            
            webcam_placeholder = st.empty()
            
            run_cam = st.checkbox("웹캠 활성화", key="webcam_toggle_rtm")
            
            if "webcam_running_rtm" not in st.session_state:
                st.session_state.webcam_running_rtm = False

            if run_cam and not st.session_state.webcam_running_rtm:
                st.session_state.webcam_running_rtm = True
                cam = cv2.VideoCapture(0) # 0 for default webcam
                
                if not cam.isOpened():
                    st.error("❌ 웹캠을 열 수 없습니다. 카메라가 연결되어 있는지 확인하세요.")
                    st.session_state.webcam_running_rtm = False
                else:
                    st.info("웹캠 스트리밍 시작...")
                    frame_count = 0 # Initialize frame counter for stride
                    while st.session_state.webcam_running_rtm:
                        ret, frame = cam.read()
                        if not ret:
                            st.warning("웹캠 프레임 읽기 실패.")
                            break
                        
                        if frame_count % stride == 0: # Apply stride
                            result = processor.process_frame(frame)
                            webcam_placeholder.image(result["annotated_frame"], channels="BGR", caption="Live Webcam Feed")
                            
                            if result["is_danger"]:
                                status_indicator.error("⚠️ DANGER")
                                alert_box.markdown("🚨 **Violence / Abuse Detected!**")
                            else:
                                status_indicator.success("✅ Normal")
                                alert_box.empty()
                            score_gauge.metric("Danger Score", f"{result['danger_score']:.2f}")
                        frame_count += 1 # Increment frame count regardless of stride
                            
                    cam.release()
                    st.session_state.webcam_running_rtm = False
                    st.info("웹캠 스트리밍 중지.")
            elif not run_cam and st.session_state.webcam_running_rtm:
                st.session_state.webcam_running_rtm = False
                st.info("웹캠 비활성화 요청됨.")

if __name__ == "__main__":
    app()