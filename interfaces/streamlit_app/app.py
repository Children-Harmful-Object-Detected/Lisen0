# ============================================================================
# LiSEN Dashboard - Main App Orchestrator
# ============================================================================
import streamlit as st
from pathlib import Path
import sys

# --- Project Setup ---
# Windows Path Fix for torch.load, must be first in some cases
import os
if os.name == 'nt':
    import pathlib
    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

# Load config
from core.utils import load_config, resolve_path
CONFIG_PATH = PROJECT_ROOT / "config.yaml"
try:
    config = load_config(str(CONFIG_PATH))
except Exception as e:
    st.error(f"❌ 설정 파일(config.yaml) 로드 실패: {e}")
    st.stop()

# Define major directories from config
DATA_RAW_REL = config['paths']['data']['raw_videos']
DATA_RAW = resolve_path(str(CONFIG_PATH), DATA_RAW_REL)

MODEL_YOLO = resolve_path(str(CONFIG_PATH), config['paths']['models']['yolo_champion'])
MODEL_TF_REL = config['paths']['models']['transformer_judge']
MODEL_TF = resolve_path(str(CONFIG_PATH), MODEL_TF_REL)

# Define other directories based on project root (legacy structure)
DATA_PROC = PROJECT_ROOT / "data" / "processed"
RESULTS_DIR = PROJECT_ROOT / "results"
FEATURE_DIR = DATA_PROC / "features"
MODEL_DIR = PROJECT_ROOT / "models" # Base model dir for saving/legacy access

# Ensure directories exist
for d in [DATA_PROC, DATA_RAW, MODEL_DIR, RESULTS_DIR, FEATURE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# --- Page Config ---
st.set_page_config(
    page_title="LiSEN Workflow Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom Module Imports ---
from interfaces.streamlit_app.common.sidebar import render_sidebar
from interfaces.streamlit_app.tabs import (
    tab0, tab1, tab2, tab3, tab4, tab5,
    tab6, tab7, tab8, tab9, tab10, tab11, tab12
)

# --- Main App ---
render_sidebar()

# Debug info in sidebar
with st.sidebar:
    with st.expander("🛠️ Debug Info", expanded=False):
        st.success("✅ Config Loaded")
        st.text(f"Raw Data: .../{DATA_RAW.parent.name}/{DATA_RAW.name}")
        st.text(f"YOLO Model: {MODEL_YOLO.name}")
        st.text(f"TF Model: {MODEL_TF.name}")

st.title("🧬 LiSEN")

# --- Welcome Screen & Background ---
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e3f2fd, #fce4ec);
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: linear-gradient(135deg, #e3f2fd, #fce4ec) !important;
}
[data-testid="stDecoration"] {
    background: linear-gradient(135deg, #e3f2fd, #fce4ec) !important;
}
header[data-testid="stHeader"] { height: 60px; }
.block-container { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

if "show_tabs" not in st.session_state:
    st.session_state.show_tabs = False

if not st.session_state.show_tabs:
    st.markdown(
        """
        <div style='text-align:center; padding-top:50px;'>
        <h1 style='font-size:48px; font-weight:800;'>👋 환영합니다!</h1>
        <h3 style='color:#555; margin-top:-10px; font-weight:600;'>LiSEN AI Workflow Dashboard</h3>
        <p style='font-size:18px; color:#444; margin-top:25px;'>YOLO Pose · Transformer 기반 위험도 분석 AI 워크플로우입니다.</p>
        <img src='https://em-content.zobj.net/source/microsoft-teams/337/robot_1f916.png' width='130' style='margin-top:30px; opacity:0.95;'>
        <p style='font-size:17px; color:#555; margin-top:30px;'>아래 버튼을 눌러 워크플로우를 시작하세요.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns([2, 4, 2])
    with col2:
        if st.button("🚀 시작하기", use_container_width=True):
            st.session_state.show_tabs = True
            st.rerun()
    st.stop()


# --- Tab Definitions ---
TABS = st.tabs([
    "0️⃣ 튜토리얼",
    "1️⃣ Pose 라벨링",
    "2️⃣ 데이터 검증",
    "3️⃣ YOLO 학습",
    "4️⃣ 행동 라벨링",
    "5️⃣ 시퀀스 생성",
    "6️⃣ 데이터 증강",
    "7️⃣ Transformer 학습",
    "8️⃣ 모델 추론",
    "9️⃣ 실시간 위험 감지",
    "🔟 직접 추론",
    "1️⃣1️⃣ 게시판",
    "🔬 V2 실험실",
])

# --- Tab Rendering ---
with TABS[0]:
    tab0.render_tab(DATA_RAW)
with TABS[1]:
    tab1.render_tab(DATA_RAW, MODEL_DIR, DATA_PROC)
with TABS[2]:
    tab2.render_tab(DATA_PROC)
with TABS[3]:
    tab3.render_tab(DATA_PROC, MODEL_DIR, RESULTS_DIR)
with TABS[4]:
    tab4.render_tab(DATA_RAW, DATA_PROC)
with TABS[5]:
    tab5.render_tab(DATA_PROC, FEATURE_DIR)
with TABS[6]:
    tab6.render_tab(DATA_PROC)
with TABS[7]:
    tab7.render_tab(DATA_PROC, MODEL_DIR)
with TABS[8]:
    tab8.render_tab(MODEL_YOLO, MODEL_DIR, DATA_PROC)
with TABS[9]:
    tab9.render_tab(RESULTS_DIR)
with TABS[10]:
    tab10.render_tab(MODEL_YOLO, MODEL_DIR, RESULTS_DIR)
with TABS[11]:
    tab11.render_tab(PROJECT_ROOT)
with TABS[12]:
    tab12.render_tab(MODEL_DIR, DATA_PROC)
