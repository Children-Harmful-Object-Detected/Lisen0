import streamlit as st
from interfaces.streamlit_app.modules.action_dataset_builder import build_action_sequences

def render_tab(DATA_PROC, FEATURE_DIR):
    """Renders the content for Tab 5: Action Pose Sequence Generation."""
    st.header("📈 시퀀스 생성 (Action Pose Sequence)")

    if st.button("▶ 시퀀스 생성 실행"):
        build_action_sequences(DATA_PROC, FEATURE_DIR)
        # The success message is within the build_action_sequences function, so no need to repeat it here.
