import streamlit as st
import matplotlib.pyplot as plt
from interfaces.streamlit_app.modules.data_validation import (
    validate_image_label_pairs,
    validate_label_values,
    collect_class_distribution,
)

def render_tab(DATA_PROC):
    """Renders the content for Tab 2: Data Validation."""
    st.header("🧹 데이터 검증 / 정제")

    if st.button("🧪 검증 실행"):
        st.subheader("🔍 이미지 / 라벨 매칭")
        st.json(validate_image_label_pairs(DATA_PROC))

        st.markdown("---")
        st.subheader("🔎 YOLO 라벨 값 검증")

        errors = {}
        for split in ["train", "val"]:
            for lbl in (DATA_PROC / f"labels/{split}").glob("*.txt"):
                err = validate_label_values(lbl)
                if err:
                    errors[str(lbl)] = err

        if errors:
            st.error("⚠ 오류 라벨 발견")
            st.json(errors)
        else:
            st.success("✔ 모든 라벨 정상")

        st.markdown("---")
        st.subheader("📊 Adult/Child 클래스 분포")

        dist = collect_class_distribution(DATA_PROC)
        fig, ax = plt.subplots(figsize=(4, 2))
        ax.bar(list(dist.keys()), list(dist.values()), color="#3498db")
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["Adult", "Child"])
        st.pyplot(fig)
