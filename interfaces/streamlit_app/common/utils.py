import pandas as pd
from pathlib import Path
import streamlit as st

def scan_raw_data(root: Path):
    return {
        "mp4": sorted(root.rglob("*.mp4")),
        "json": sorted(root.rglob("*.json")),
        "csv": sorted(root.rglob("*.csv")),
        "images": sorted(list(root.rglob("*.jpg")) + list(root.rglob("*.png"))),
    }

def render_data_overview(stats: dict):
    df = pd.DataFrame({
        "Type": ["영상(mp4)", "JSON", "CSV", "이미지"],
        "Count": [
            len(stats["mp4"]),
            len(stats["json"]),
            len(stats["csv"]),
            len(stats["images"]),
        ]
    })
    st.dataframe(df, use_container_width=True)

def render_project_summary():
    st.markdown("""
    - **1️⃣ Pose 라벨링** — `Lisen.pt` (YOLO Pose 모델)로 Adult/Child + Keypoints 라벨을 자동 생성합니다.
    - **2️⃣ 데이터 검증** — 생성된 라벨 값 오류 및 이미지-라벨 매칭을 검증합니다.
    - **3️⃣ YOLO 학습** — `Lisen.pt` (YOLO Pose 모델)을 사용하여 Adult/Child 분류 모델을 학습합니다.
    - **4️⃣ 행동 라벨링** — 각 프레임의 행동(Action)을 직접 입력하고 관리합니다.
    - **5️⃣ 시퀀스 생성** — Pose keypoint를 Transformer 입력 시퀀스로 변환합니다.
    - **6️⃣ 데이터 증강** — Pose 시퀀스에 증강(jitter, flip 등)을 적용합니다.
    - **7️⃣ Transformer 학습** — 행동 라벨 기반 위험도 분류 Transformer 모델을 학습합니다.
    - **8️⃣ 모델 추론** — `Lisen.pt`와 Transformer 모델을 결합하여 영상 위험도를 분석하고 프레임별 상세 정보를 제공합니다.
    - **9️⃣ 실시간 위험 감지** — 분석된 영상 기반으로 위험도 변화를 모니터링합니다.
    - **📋 게시판** — 사용자 메모 및 기록을 저장하고 공유하는 간단한 게시판입니다.
    - **📹 Realtime Monitor (사이드바 메뉴)** — `Lisen.pt`와 Transformer를 활용하여 실시간으로 비디오 파일 또는 웹캠을 통한 위험 행동을 모니터링합니다.
    """)

def render_file_list(files: list[Path], base_dir: Path):
    """Renders a list of files with their paths relative to a base directory."""
    if not files:
        st.info("해당 종류의 파일이 없습니다.")
        return

    # Display as a list with relative paths
    for f in files:
        try:
            relative_p = f.relative_to(base_dir)
            st.code(str(relative_p), language=None)
        except ValueError:
            st.code(str(f), language=None)