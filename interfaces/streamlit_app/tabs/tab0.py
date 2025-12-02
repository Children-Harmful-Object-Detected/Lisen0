import streamlit as st
from interfaces.streamlit_app.common.utils import scan_raw_data, render_data_overview, render_project_summary

def render_tab(DATA_RAW):
    """Renders the content for Tab 0: Project Summary and Data Exploration."""
    st.header("📁 프로젝트 요약")
    render_project_summary()

    st.markdown("---")

    st.header("📊 데이터 탐색")
    stats = scan_raw_data(DATA_RAW)
    render_data_overview(stats)
