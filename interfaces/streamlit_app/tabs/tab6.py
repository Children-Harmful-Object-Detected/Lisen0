import streamlit as st
import numpy as np
from interfaces.streamlit_app.modules.dataset_augmentation import (
    load_sequence_dataset,
    apply_sequence_augmentations,
    save_augmented_dataset
)

def render_tab(DATA_PROC):
    """Renders the content for Tab 6: Sequence Data Augmentation."""
    st.header("🧪 시퀀스 데이터 증강 ")

    seq_file = DATA_PROC / "action_sequences" / "dataset_action_pose.npz"

    if not seq_file.exists():
        st.error(f"❌ 시퀀스 파일 없음: {seq_file}")
        return

    X, Y = load_sequence_dataset(seq_file)

    st.write(f"**시퀀스 개수:** {len(X)}")
    st.write(f"**시퀀스 길이:** {X.shape[1]}")
    st.write(f"**Feature 수:** {X.shape[2]}")

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:  use_flip = st.checkbox("좌우 반전", True, key="aug_flip")
    with col2:  use_jitter = st.checkbox("노이즈", True, key="aug_jitter")
    with col3:  use_scale = st.checkbox("스케일", True, key="aug_scale")
    with col4:  use_shift = st.checkbox("Shift", True, key="aug_shift")

    aug_count = st.slider("증강 횟수", 1, 10, 3, key="aug_count")

    if st.button("🚀 시퀀스 증강 실행"):
        with st.spinner("증강 생성 중..."):
            X_aug, Y_aug = apply_sequence_augmentations(
                X, Y,
                aug_count=aug_count,
                use_flip=use_flip,
                use_jitter=use_jitter,
                use_scale=use_scale,
                use_shift=use_shift
            )

            X_final = np.concatenate([X, X_aug], axis=0)
            Y_final = np.concatenate([Y, Y_aug], axis=0)

            save_path = DATA_PROC / "action_sequences" / "dataset_action_pose_aug.npz"
            save_augmented_dataset(X_final, Y_final, save_path)

        st.success(f"🎉 저장됨 → {save_path.name}")
