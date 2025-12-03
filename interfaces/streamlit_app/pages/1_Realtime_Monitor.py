import streamlit as st
import cv2
import tempfile
import numpy as np
from pathlib import Path
import sys
import time
<<<<<<< HEAD
import pandas as pd
import altair as alt

# --- Project-specific Imports ---
from core.utils import load_config, resolve_path
from core.realtime_processor import RealtimeVideoProcessor

# Determine PROJECT_ROOT relative to this page file
PAGE_FILE_PATH = Path(__file__).resolve()
STREAMLIT_APP_DIR = PAGE_FILE_PATH.parent.parent 
INTERFACES_DIR = STREAMLIT_APP_DIR.parent 
PROJECT_ROOT = INTERFACES_DIR.parent 

# Config Path
=======

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
>>>>>>> 7e1f10b3d9713a69b94b2694c8247664e7e86193
CONFIG_PATH = PROJECT_ROOT / "config.yaml"

# Load Config
try:
    config = load_config(str(CONFIG_PATH))
except Exception as e:
    st.error(f"❌ 설정 파일 로드 실패: {e}")
    st.stop()

<<<<<<< HEAD
# Resolve Model Paths
=======
# Resolve Model Paths from config
>>>>>>> 7e1f10b3d9713a69b94b2694c8247664e7e86193
MODEL_YOLO_PATH = resolve_path(str(CONFIG_PATH), config['paths']['models']['yolo_champion'])
MODEL_TF_PATH = resolve_path(str(CONFIG_PATH), config['paths']['models']['transformer_judge'])


<<<<<<< HEAD
def app(): 
=======
def app(): # Renamed main() to app() for Streamlit multi-page app convention
>>>>>>> 7e1f10b3d9713a69b94b2694c8247664e7e86193
    st.set_page_config(page_title="Real-time Monitor", page_icon="📹", layout="wide")
    st.title("📹 Real-time Intelligence Monitor")
    
    # Sidebar Options
    st.sidebar.header("Monitor Settings")
<<<<<<< HEAD
=======
    
>>>>>>> 7e1f10b3d9713a69b94b2694c8247664e7e86193
    st.sidebar.text(f"Combined YOLO Model: {MODEL_YOLO_PATH.name}")
    st.sidebar.text(f"Transformer Model: {MODEL_TF_PATH.name}")
    
    conf_thres = st.sidebar.slider("Confidence Threshold", 0.1, 0.9, 0.5, 0.05, key="conf_thres_rtm")
<<<<<<< HEAD
    stride = st.sidebar.slider("프레임 간격 (Stride)", 1, 15, 1, key="frame_stride_rtm") 
    
    # Initialize Session State
    if "chart_data" not in st.session_state:
        st.session_state.chart_data = pd.DataFrame(columns=["Frame", "Violence (YOLO)", "Non-Violence (YOLO)", "TF Safety Prob", "TF Warning Prob", "TF Danger Prob", "Danger (Final)", "User Tag"])
    if "tag_log" not in st.session_state:
        st.session_state.tag_log = []
    if "current_tag_start" not in st.session_state:
        st.session_state.current_tag_start = None
=======
    stride = st.sidebar.slider("프레임 간격 (Stride)", 1, 15, 1, key="frame_stride_rtm") # New stride setting
>>>>>>> 7e1f10b3d9713a69b94b2694c8247664e7e86193
    
    # Input Source
    input_source = st.sidebar.radio("Input Source", ["Upload Video", "Webcam"], key="input_source_rtm")

<<<<<<< HEAD
    # ... (Start frame logic) ...
=======
    # --- Start Frame Setting for Upload Video ---
>>>>>>> 7e1f10b3d9713a69b94b2694c8247664e7e86193
    start_frame = 0
    if input_source == "Upload Video":
        st.sidebar.markdown("---")
        st.sidebar.subheader("Video Analysis Start Point")
<<<<<<< HEAD
        if "current_start_frame_rtm" not in st.session_state:
            st.session_state.current_start_frame_rtm = 0
        start_frame_input = st.sidebar.number_input("Start Frame", min_value=0, value=st.session_state.current_start_frame_rtm, step=10, key="start_frame_input_rtm")
        st.session_state.current_start_frame_rtm = start_frame_input
        start_frame = start_frame_input
        
        col_prev, col_next = st.sidebar.columns(2)
        with col_prev:
            if st.button("-100 Frames"): st.session_state.current_start_frame_rtm = max(0, st.session_state.current_start_frame_rtm - 100); st.rerun()
            if st.button("-50 Frames"): st.session_state.current_start_frame_rtm = max(0, st.session_state.current_start_frame_rtm - 50); st.rerun()
            if st.button("-10 Frames"): st.session_state.current_start_frame_rtm = max(0, st.session_state.current_start_frame_rtm - 10); st.rerun()
        with col_next:
            if st.button("+10 Frames"): st.session_state.current_start_frame_rtm += 10; st.rerun()
            if st.button("+50 Frames"): st.session_state.current_start_frame_rtm += 50; st.rerun()
            if st.button("+100 Frames"): st.session_state.current_start_frame_rtm += 100; st.rerun()

    # Processor Init
=======
        
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
>>>>>>> 7e1f10b3d9713a69b94b2694c8247664e7e86193
    @st.cache_resource
    def get_realtime_processor(yolo_path, tf_path, conf):
        return RealtimeVideoProcessor(yolo_path, tf_path, conf)

    try:
        processor = get_realtime_processor(MODEL_YOLO_PATH, MODEL_TF_PATH, conf_thres)
<<<<<<< HEAD
        processor.conf_threshold = conf_thres 
=======
        processor.conf_threshold = conf_thres # Dynamic update of threshold
>>>>>>> 7e1f10b3d9713a69b94b2694c8247664e7e86193
    except Exception as e:
        st.error(f"❌ 모델 로드 오류: {e}")
        st.stop()

<<<<<<< HEAD
    # Layout
    col_video, col_stats = st.columns([3, 1])

    with col_stats:
        # Manual Control Section
        st.markdown("### 🕹️ Manual Control")
        is_tagging_on = st.toggle("🚩 Tag Violence (Manual)", key="tag_toggle_rtm")
        
        current_frame_approx = st.session_state.get("current_processing_frame", 0)
        if is_tagging_on and st.session_state.current_tag_start is None:
            st.session_state.current_tag_start = current_frame_approx
        elif not is_tagging_on and st.session_state.current_tag_start is not None:
            st.session_state.tag_log.append({"Start Frame": st.session_state.current_tag_start, "End Frame": current_frame_approx})
            st.session_state.current_tag_start = None

        if st.button("🔴 Force Stop (강제 종료)", key="force_stop_rtm"):
            st.stop()
            
        st.markdown("### 📝 Tag Log")
        if st.session_state.tag_log:
            st.dataframe(pd.DataFrame(st.session_state.tag_log), height=150)
            if st.button("💾 Save & Reset Tags"):
                save_dir = PROJECT_ROOT / "results" / "tag_logs"
                save_dir.mkdir(parents=True, exist_ok=True)
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                save_path = save_dir / f"manual_tags_{timestamp}.csv"
                pd.DataFrame(st.session_state.tag_log).to_csv(save_path, index=False)
                st.success(f"Saved to {save_path.name}")
                st.session_state.tag_log = []
                time.sleep(1)
                st.rerun()
        else:
            st.info("No tags recorded.")
            
        st.markdown("---")
        if st.button("📊 탐지 분석 오차 확인", key="verify_btn"):
            if st.session_state.tag_log and not st.session_state.chart_data.empty:
                df = st.session_state.chart_data
                tags = st.session_state.tag_log
                sector_stats = []
                total_tagged_frames = 0
                total_detected_frames = 0
                for idx, tag in enumerate(tags):
                    start = tag['Start Frame']
                    end = tag['End Frame']
                    sector_df = df[(df['Frame'] >= start) & (df['Frame'] <= end)]
                    sector_len = len(sector_df)
                    if sector_len > 0:
                        detected_count = len(sector_df[sector_df['Danger (Final)'] > 0.5])
                        match_rate = (detected_count / sector_len) * 100
                        sector_stats.append({"Sector": f"#{idx+1}", "Duration": sector_len, "Detected": detected_count, "Match (%)": f"{match_rate:.1f}%"})
                        total_tagged_frames += sector_len
                        total_detected_frames += detected_count
                global_rate = (total_detected_frames / total_tagged_frames * 100) if total_tagged_frames > 0 else 0.0
                st.markdown("#### 🎯 분석 결과")
                st.metric("Global Match Rate", f"{global_rate:.1f}%")
                st.dataframe(pd.DataFrame(sector_stats))
                
                # --- Visual Verification Chart ---
                st.markdown("#### 📉 구간 시각화 (Visual Verification)")
                
                # Reuse Logic to build chart
                display_df = df.copy()
                
                # Ensure User Tag is present (from logs)
                display_df["User Tag"] = 0.0
                for tag in tags:
                    display_df.loc[(display_df["Frame"] >= tag['Start Frame']) & (display_df["Frame"] <= tag['End Frame']), "User Tag"] = 1.0
                
                # Ensure Model Detect is present
                display_df["Model Detect"] = 0.0
                if "Danger (Final)" in display_df.columns:
                    display_df.loc[display_df["Danger (Final)"] > 0.5, "Model Detect"] = 1.0
                
                # Ensure Match is present
                display_df["Match"] = 0.0
                match_mask = (display_df["User Tag"] == 1.0) & (display_df["Model Detect"] == 1.0)
                display_df.loc[match_mask, "Match"] = 1.0
                
                # Build Chart
                base = alt.Chart(display_df).encode(x='Frame:Q')
                layers = []
                # Red: User Tag
                layers.append(base.mark_area(opacity=0.3, color='red', interpolate='step').encode(y=alt.Y('User Tag:Q', title='User Tag', axis=alt.Axis(format=".1f")))) # Add axis title, format
                # Blue: Model Detect
                layers.append(base.mark_area(opacity=0.3, color='blue', interpolate='step').encode(y=alt.Y('Model Detect:Q', title='Model Detect', axis=alt.Axis(format=".1f")))) # Add axis title, format
                # Green: Match
                layers.append(base.mark_area(opacity=0.6, color='#00FF00', interpolate='step').encode(y=alt.Y('Match:Q', title='Match', axis=alt.Axis(format=".1f")))) # Add axis title, format
                # Lines
                # selected_metrics list should be available in session state if multiselect is used.
                # If not, use a default list. For verification, all lines should be visible for context.
                all_metrics_for_verification = ["Violence (YOLO)", "Non-Violence (YOLO)", "TF Safety Prob", "TF Warning Prob", "TF Danger Prob", "Danger (Final)"]
                lines = base.transform_fold(all_metrics_for_verification, as_=['Metric', 'Value']).mark_line().encode(y=alt.Y('Value:Q', title='Value', axis=alt.Axis(format=".1f")), color='Metric:N', tooltip=['Frame:Q', 'Metric:N', 'Value:Q']) # Remove fixed domain, add title
                layers.append(lines)

                st.altair_chart(alt.layer(*layers).properties(height=350).interactive(), use_container_width=True)

            else:
                st.warning("데이터 부족")

        st.markdown("---")
        st.subheader("데이터 내보내기 (Export Data)")
        if not st.session_state.chart_data.empty:
            csv_data = st.session_state.chart_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📊 차트 데이터 CSV 다운로드",
                data=csv_data,
                file_name=f"realtime_chart_data_{time.strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key="download_chart_data_csv"
            )
        else:
            st.info("내보낼 차트 데이터가 없습니다.")

        st.markdown("---")
=======
    # Main Display Area
    col_video, col_stats = st.columns([3, 1])

    with col_stats:
>>>>>>> 7e1f10b3d9713a69b94b2694c8247664e7e86193
        st.subheader("Live Stats")
        status_indicator = st.empty()
        score_gauge = st.empty()
        alert_box = st.empty()

    with col_video:
        stframe = st.empty()
<<<<<<< HEAD
        st.markdown("### 📈 Real-time Risk Analysis")
        
        # Chart Controls
        all_metrics = ["Violence (YOLO)", "Non-Violence (YOLO)", "TF Safety Prob", "TF Warning Prob", "TF Danger Prob", "Danger (Final)"]
        selected_metrics = st.multiselect("표시할 그래프 요소 선택", options=all_metrics, default=["Violence (YOLO)", "TF Danger Prob", "Danger (Final)"], key="chart_metric_select")
        
        chart_placeholder = st.empty()

        # Prepare & Render Chart (Initial / Re-render)
        display_df = st.session_state.chart_data.copy() if "chart_data" in st.session_state else pd.DataFrame()
        if not display_df.empty:
            # Apply User Tags (Ground Truth)
            display_df["User Tag"] = 0.0
            if st.session_state.tag_log:
                for tag in st.session_state.tag_log:
                    display_df.loc[(display_df["Frame"] >= tag['Start Frame']) & (display_df["Frame"] <= tag['End Frame']), "User Tag"] = 1.0
            
            # Calculate Model Detection (Prediction)
            display_df["Model Detect"] = 0.0
            if "Danger (Final)" in display_df.columns:
                display_df.loc[display_df["Danger (Final)"] > 0.5, "Model Detect"] = 1.0
            
            # Calculate Match (Overlap)
            display_df["Match"] = 0.0
            match_mask = (display_df["User Tag"] == 1.0) & (display_df["Model Detect"] == 1.0)
            display_df.loc[match_mask, "Match"] = 1.0

            base = alt.Chart(display_df).encode(x='Frame:Q') # Frame is Quantitative
            layers = []
            
            # Layer A: User Tag Area (Red, Semi-transparent)
            tag_area = base.mark_area(opacity=0.3, color='red', interpolate='step').encode(
                y=alt.Y('User Tag:Q', title='User Tag', axis=alt.Axis(format=".1f")), # Add axis, format
                tooltip=['Frame:Q', 'User Tag:Q']
            )
            layers.append(tag_area)
            
            # Layer B: Model Detect Area (Blue, Semi-transparent)
            pred_area = base.mark_area(opacity=0.3, color='blue', interpolate='step').encode(
                y=alt.Y('Model Detect:Q', title='Model Detect', axis=alt.Axis(format=".1f")) # Add axis, format
            )
            layers.append(pred_area)
            
            # Layer C: Match Area (Green, Opaque)
            match_area = base.mark_area(opacity=0.6, color='#00FF00', interpolate='step').encode(
                y=alt.Y('Match:Q', title='Match', axis=alt.Axis(format=".1f")) # Add axis, format
            )
            layers.append(match_area)
            
            # Layer D: Selected Lines
            if selected_metrics:
                lines = base.transform_fold(
                    selected_metrics,
                    as_=['Metric', 'Value']
                ).mark_line().encode(
                    y=alt.Y('Value:Q', title='Value', axis=alt.Axis(format=".1f")), # Remove fixed domain, add title
                    color='Metric:N',
                    tooltip=['Frame:Q', 'Metric:N', 'Value:Q'] # Explicit types for tooltip
                )
                layers.append(lines)
            
            combined_chart = alt.layer(*layers).properties(height=350).interactive()
            chart_placeholder.altair_chart(combined_chart, use_container_width=True)
        else:
            chart_placeholder.info("Waiting for data...")

=======
        
>>>>>>> 7e1f10b3d9713a69b94b2694c8247664e7e86193
        if input_source == "Upload Video":
            uploaded_file = st.file_uploader("Choose a video file...", type=["mp4", "avi", "mov"], key="uploaded_file_rtm")
            
            if uploaded_file is not None:
<<<<<<< HEAD
=======
                # Save uploaded file to temp
>>>>>>> 7e1f10b3d9713a69b94b2694c8247664e7e86193
                tfile = tempfile.NamedTemporaryFile(delete=False) 
                tfile.write(uploaded_file.read())
                
                vf = cv2.VideoCapture(tfile.name)
                total_frames = int(vf.get(cv2.CAP_PROP_FRAME_COUNT))
                
<<<<<<< HEAD
                if start_frame >= total_frames: start_frame = total_frames - 1
                st.sidebar.info(f"Total Frames: {total_frames}")
                st.sidebar.number_input("Start Frame (Adj)", value=start_frame, disabled=True)
=======
                # Adjust start_frame if it exceeds total_frames
                if start_frame >= total_frames:
                    start_frame = total_frames - 1
                    st.sidebar.warning(f"시작 프레임이 총 프레임({total_frames})을 초과하여 {start_frame}으로 조정됩니다.")

                st.sidebar.info(f"선택 영상 총 프레임: {total_frames}")
                st.sidebar.number_input("조정된 시작 프레임", value=start_frame, disabled=True, key="display_start_frame_rtm")

>>>>>>> 7e1f10b3d9713a69b94b2694c8247664e7e86193

                start_button = st.button("▶ Start Analysis", key="start_rtm")
                stop_button = st.button("⏹ Stop", key="stop_rtm")
                
<<<<<<< HEAD
                if "stop_analysis_rtm" not in st.session_state: st.session_state.stop_analysis_rtm = False
                if stop_button: st.session_state.stop_analysis_rtm = True
                if start_button:
                    st.session_state.stop_analysis_rtm = False 
                    st.session_state.is_running = True
                    st.session_state.chart_data = pd.DataFrame(columns=["Frame", "Violence (YOLO)", "Non-Violence (YOLO)", "TF Safety Prob", "TF Warning Prob", "TF Danger Prob", "Danger (Final)", "User Tag"])
                    st.session_state.tag_log = []
                    st.session_state.current_tag_start = None

                if st.session_state.get("is_running", False) and not st.session_state.stop_analysis_rtm:
                    if "current_processing_frame" not in st.session_state: st.session_state.current_processing_frame = start_frame
                    if start_button: st.session_state.current_processing_frame = start_frame

                    vf.set(cv2.CAP_PROP_POS_FRAMES, st.session_state.current_processing_frame)
                    frame_count = st.session_state.current_processing_frame 
                    
                    while vf.isOpened() and not st.session_state.stop_analysis_rtm:
                        ret, frame = vf.read()
                        if not ret:
                            st.session_state.is_running = False
                            break

                        if frame_count % stride == 0: 
                            result = processor.process_frame(frame) 
                            stframe.image(result["annotated_frame"], channels="BGR")
                            
                            new_row = pd.DataFrame({
                                "Frame": [frame_count],
                                "Violence (YOLO)": [result['violence_score_obj_det']],
                                "Non-Violence (YOLO)": [result['nonviolence_score_obj_det']],
                                "TF Safety Prob": [result['risk_probs'][0]],
                                "TF Warning Prob": [result['risk_probs'][1]],
                                "TF Danger Prob": [result['risk_probs'][2]],
                                "Danger (Final)": [result['danger_score']],
                                "User Tag": [1.0 if is_tagging_on else 0.0]
                            })
                            st.session_state.chart_data = pd.concat([st.session_state.chart_data, new_row], ignore_index=True)
                            
                            # Update Chart in Loop (Altair)
                            current_df = st.session_state.chart_data.copy()
                            if not current_df.empty:
                                # Calculate Model Detect for Visualization
                                current_df["Model Detect"] = 0.0
                                if "Danger (Final)" in current_df.columns:
                                    current_df.loc[current_df["Danger (Final)"] > 0.5, "Model Detect"] = 1.0

                                base = alt.Chart(current_df).encode(x='Frame:Q')
                                chart_layers = []
                                # User Tag Area
                                chart_layers.append(base.mark_area(opacity=0.3, color='red', interpolate='step').encode(y=alt.Y('User Tag:Q', title='User Tag', axis=alt.Axis(format=".1f"))))
                                # Model Detect Area (Blue)
                                chart_layers.append(base.mark_area(opacity=0.3, color='blue', interpolate='step').encode(y=alt.Y('Model Detect:Q', title='Model Detect', axis=alt.Axis(format=".1f"))))
                                # Lines
                                if selected_metrics:
                                    chart_layers.append(base.transform_fold(selected_metrics, as_=['Metric', 'Value']).mark_line().encode(y=alt.Y('Value:Q', title='Value', axis=alt.Axis(format=".1f")), color='Metric:N'))
                                chart_placeholder.altair_chart(alt.layer(*chart_layers).properties(height=350), use_container_width=True)

                            if result["is_danger"]: 
                                status_indicator.error(f"🔴 DANGER ({result['danger_score']:.2f})")
                                alert_box.markdown("🚨 **Violence / Abuse Detected!**")
                            elif result["risk_label"] == "Warning": 
                                status_indicator.warning(f"🟡 WARNING ({result['risk_score_transformer']:.2f})")
                                alert_box.empty()
                            else: 
                                status_indicator.success(f"🟢 SAFETY ({result['risk_score_transformer']:.2f})")
                                alert_box.empty()
                            score_gauge.metric("Danger Score", f"{result['danger_score']:.2f}")
                        
                        frame_count += 1 
                        st.session_state.current_processing_frame = frame_count
                            
                    vf.release()
                    if not st.session_state.is_running: st.success("Analysis Complete.")

        elif input_source == "Webcam":
            # Webcam Logic (Same structure)
            st.info("Webcam requires local camera access.")
            webcam_placeholder = st.empty()
            run_cam = st.checkbox("Enable Webcam", key="webcam_toggle_rtm")
            
            if "webcam_running_rtm" not in st.session_state: st.session_state.webcam_running_rtm = False
            if run_cam and not st.session_state.webcam_running_rtm:
                st.session_state.webcam_running_rtm = True
                cam = cv2.VideoCapture(0)
                if not cam.isOpened():
                    st.error("Webcam Error")
                    st.session_state.webcam_running_rtm = False
                else:
                    st.info("Streaming...")
                    frame_count = 0
                    st.session_state.chart_data = pd.DataFrame(columns=["Frame", "Violence (YOLO)", "Non-Violence (YOLO)", "TF Safety Prob", "TF Warning Prob", "TF Danger Prob", "Danger (Final)", "User Tag"])
                    
                    while st.session_state.webcam_running_rtm:
                        ret, frame = cam.read()
                        if not ret: break
                        
                        if frame_count % stride == 0:
                            result = processor.process_frame(frame)
                            webcam_placeholder.image(result["annotated_frame"], channels="BGR")
                            
                            new_row = pd.DataFrame({
                                "Frame": [frame_count],
                                "Violence (YOLO)": [result['violence_score_obj_det']],
                                "Non-Violence (YOLO)": [result['nonviolence_score_obj_det']],
                                "TF Safety Prob": [result['risk_probs'][0]],
                                "TF Warning Prob": [result['risk_probs'][1]],
                                "TF Danger Prob": [result['risk_probs'][2]],
                                "Danger (Final)": [result['danger_score']],
                                "User Tag": [1.0 if is_tagging_on else 0.0]
                            })
                            st.session_state.chart_data = pd.concat([st.session_state.chart_data, new_row], ignore_index=True)
                            
                            # Update Chart in Loop (Altair)
                            current_df = st.session_state.chart_data.copy()
                            if not current_df.empty:
                                # Calculate Model Detect for Visualization
                                current_df["Model Detect"] = 0.0
                                if "Danger (Final)" in current_df.columns:
                                    current_df.loc[current_df["Danger (Final)"] > 0.5, "Model Detect"] = 1.0

                                base = alt.Chart(current_df).encode(x='Frame:Q')
                                chart_layers = []
                                # User Tag Area
                                chart_layers.append(base.mark_area(opacity=0.3, color='red', interpolate='step').encode(y=alt.Y('User Tag:Q', title='User Tag', axis=alt.Axis(format=".1f"))))
                                # Model Detect Area (Blue)
                                chart_layers.append(base.mark_area(opacity=0.3, color='blue', interpolate='step').encode(y=alt.Y('Model Detect:Q', title='Model Detect', axis=alt.Axis(format=".1f"))))
                                # Lines
                                if selected_metrics:
                                    chart_layers.append(base.transform_fold(selected_metrics, as_=['Metric', 'Value']).mark_line().encode(y=alt.Y('Value:Q', title='Value', axis=alt.Axis(format=".1f")), color='Metric:N'))
                                chart_placeholder.altair_chart(alt.layer(*chart_layers).properties(height=350), use_container_width=True)
                            
                            if result["is_danger"]: 
                                status_indicator.error(f"🔴 DANGER ({result['danger_score']:.2f})")
                            elif result["risk_label"] == "Warning": 
                                status_indicator.warning(f"🟡 WARNING ({result['risk_score_transformer']:.2f})")
                            else: 
                                status_indicator.success(f"🟢 SAFETY ({result['risk_score_transformer']:.2f})")
                            score_gauge.metric("Danger Score", f"{result['danger_score']:.2f}")
                        
                        frame_count += 1 
                    cam.release()
            elif not run_cam:
                st.session_state.webcam_running_rtm = False
=======
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
>>>>>>> 7e1f10b3d9713a69b94b2694c8247664e7e86193

if __name__ == "__main__":
    app()