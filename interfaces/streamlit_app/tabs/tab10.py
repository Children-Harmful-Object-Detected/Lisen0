import streamlit as st
import tempfile
import torch
from pathlib import Path
from ultralytics import YOLO
from interfaces.streamlit_app.modules.transformer import TransformerClassifier
from interfaces.streamlit_app.modules.info import analyze_video

def render_tab(MODEL_YOLO, MODEL_DIR: Path, RESULTS_DIR: Path):
    st.header("💡 직접 추론 (파일 업로드)")
    st.info("이 탭에서 동영상 파일을 업로드하면, 분석 후 결과 영상이 바로 아래에 표시됩니다.")

    uploaded_file = st.file_uploader("분석할 mp4 영상 업로드", type=["mp4"], key="direct_upload")

    if uploaded_file:
        # Save uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmpfile:
            tmpfile.write(uploaded_file.getvalue())
            temp_video_path = tmpfile.name
        
        st.info(f"업로드된 파일: {uploaded_file.name}")

        start_clicked = st.button("🚀 분석 시작", key="direct_start")
        
        if start_clicked:
            st.session_state.stop = False # Use the same session_state key `analyze_video` expects
            
            # Load models
            device = "cuda" if torch.cuda.is_available() else "cpu"
            yolo_pose = YOLO(str(MODEL_YOLO))
            yolo_box = YOLO(str(MODEL_YOLO))
            
            transformer_model_path = MODEL_DIR / "transformer_action_risk.pt"
            transformer = TransformerClassifier(input_dim=34, num_classes=3)
            transformer.load_state_dict(torch.load(transformer_model_path, map_location=device))
            transformer.to(device)
            transformer.eval()

            analyze_video(
                temp_video_path,
                yolo_pose,
                yolo_box,
                transformer,
                uploaded_file.name
            )
            
            name_stem = Path(uploaded_file.name).stem
            save_name = RESULTS_DIR / "preview" / f"preview_{name_stem}.mp4"

            if save_name.exists():
                st.success("🎉 분석 완료! 아래에서 결과 영상을 확인하세요.")
                st.video(str(save_name))
            else:
                st.error("오류: 분석 결과 영상 파일을 찾을 수 없습니다.")

    st.markdown("---")
    st.subheader("📷 웹캠 실시간 분석")

    try:
        from streamlit_webrtc import webrtc_streamer
        from interfaces.streamlit_app.modules.webcam_utils import VideoProcessor

        st.info("웹캠을 시작하려면 'Start' 버튼을 누르세요. 분석이 실시간으로 프레임에 표시됩니다.")

        webrtc_streamer(
            key="webcam",
            video_processor_factory=lambda: VideoProcessor(MODEL_DIR),
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True,
        )
    except ImportError:
        st.error("웹캠 기능을 사용하려면 'streamlit-webrtc' 라이브러리가 필요합니다.")
        st.code("pip install streamlit-webrtc")
        st.warning("위 명령어를 터미널에 입력하여 라이브러리를 설치한 후, 앱을 다시 실행해주세요.")
