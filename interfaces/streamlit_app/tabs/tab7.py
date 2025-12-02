import streamlit as st
from interfaces.streamlit_app.modules.transformer import train_transformer_model

def render_tab(DATA_PROC, MODEL_DIR):
    """Renders the content for Tab 7: Transformer Model Training."""
    st.header("🧠 Transformer 위험 행동 모델 학습")

    seq_file = DATA_PROC / "action_sequences" / "dataset_action_pose.npz"
    save_path = MODEL_DIR / "transformer_action_risk.pt"
    log_path = MODEL_DIR / "transformer_training_log.txt"

    if st.button("⚡ Transformer 학습 시작"):
        if not seq_file.exists():
            st.error("❌ 데이터셋 없음")
        else:
            with st.spinner("학습 중... 로그는 transformer_training_log.txt 에서 확인하세요."):
                acc = train_transformer_model(seq_file, save_path, log_file=log_path)
            st.success(f"🎉 완료! 최고 검증 정확도 = {acc:.3f}")
