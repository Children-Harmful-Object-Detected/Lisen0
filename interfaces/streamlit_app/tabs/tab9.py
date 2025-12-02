import streamlit as st
import json
import pandas as pd
from pathlib import Path

def render_tab(RESULTS_DIR: Path):
    """Renders the content for Tab 9: Monitoring of analyzed videos."""
    st.header("🎬 분석된 영상 기반 위험도 모니터링")

    PREVIEW_DIR = RESULTS_DIR / "preview"
    RISK_DIR = RESULTS_DIR / "risk"

    processed_videos = sorted(PREVIEW_DIR.glob("*.mp4"))

    if not processed_videos:
        st.warning("⚠️ 먼저 8번 탭에서 영상을 분석해주세요. 분석된 영상이 없습니다.")
    else:
        video_path = st.selectbox(
            "📈 모니터링할 영상을 선택하세요",
            processed_videos,
            format_func=lambda p: p.name,
            key="monitor_video_select"
        )

        if video_path:
            # Display video
            st.video(str(video_path))

            # Load and display risk data
            risk_json_path = RISK_DIR / f"{Path(video_path).stem.replace('preview_', '')}.json"

            if risk_json_path.exists():
                with open(risk_json_path, "r", encoding="utf-8") as f:
                    risk_data = json.load(f)

                df = pd.DataFrame(risk_data)
                if not df.empty:
                    df = df.set_index("time")

                    # Map labels to numerical values for charting
                    risk_map = {"Safety": 0, "Warning": 1, "Danger": 2}
                    df["risk_level"] = df["label"].map(risk_map)

                    st.markdown("### 📈 위험도 변화 그래프")
                    st.line_chart(df[["risk_level", "risk"]])

                    st.markdown("### 📋 위험도 상세 데이터")
                    st.dataframe(df)
            else:
                st.error(f"❌ 해당 영상의 위험도 데이터({risk_json_path.name})를 찾을 수 없습니다.")
