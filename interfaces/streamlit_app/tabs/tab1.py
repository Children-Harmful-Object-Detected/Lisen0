import streamlit as st
from interfaces.streamlit_app.modules.label_tools import generate_yolo_pose_labels_stream, visualize_label

def render_tab(DATA_RAW, MODEL_DIR, DATA_PROC):
    """Renders the content for Tab 1: Pose Labeling and Visualization."""
    st.header("🏷 Pose 라벨링 (Adult/Child + Keypoints)")

    videos = sorted(DATA_RAW.rglob("*.mp4"))
    if not videos:
        st.info("📁 data/raw/ 아래에 mp4 파일을 넣어주세요.")
    else:
        video_sel = st.selectbox("라벨 생성할 영상", videos)
        stride = st.slider("Stride (프레임 간격)", 1, 15, 1)

        if "stop_label" not in st.session_state:
            st.session_state.stop_label = False

        start_btn, stop_btn = st.columns([3, 1])
        start = start_btn.button("▶ 라벨 생성")
        stop_btn.button("■ 중지", on_click=lambda: st.session_state.update(stop_label=True))

        if start:
            st.session_state.stop_label = False
            pose_model = MODEL_DIR / "best.pt"

            if not pose_model.exists():
                st.error("❌ YOLO Pose 모델(best.pt)이 없습니다.")
            else:
                stframe = st.empty()
                bar = st.progress(0)
                status = st.empty()

                for annotated, idx, total in generate_yolo_pose_labels_stream(
                    video_sel, stride, pose_model, DATA_PROC
                ):
                    if st.session_state.stop_label:
                        st.warning("🛑 라벨 생성 중지됨")
                        break

                    stframe.image(annotated, channels="BGR", width=450)
                    bar.progress(int((idx + 1) / total * 100))
                    status.text(f"{idx + 1}/{total}")

                else:
                    st.success("🎉 라벨 생성 완료!")

    st.markdown("---")
    st.subheader("👀 라벨 시각화")

    split = st.selectbox("Dataset", ["train", "val"])
    img_dir = DATA_PROC / f"images/{split}"
    lbl_dir = DATA_PROC / f"labels/{split}"

    images = sorted(img_dir.glob("*.jpg"))
    if images:
        img_sel = st.selectbox("이미지 선택", images)
        if st.button("시각화 보기"):
            vis, msg = visualize_label(img_sel, lbl_dir / f"{img_sel.stem}.txt")
            st.info(msg)
            st.image(vis, channels="BGR", width=450)
