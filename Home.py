import streamlit as st
from theme import apply_theme

# 套用 Material UI 主題（深色/亮色）
apply_theme()

# ===================================
# Page Config
# ===================================
st.set_page_config(
    page_title="工程統計學 Engineering Statistics",
    page_icon="📘",
    layout="wide"
)

# ===================================
# Material UI 卡片樣式
# ===================================
st.markdown("""
<style>
.material-card {
    background-color: var(--background-color);
    padding: 1.8rem;
    border-radius: 12px;
    border: 1px solid var(--primary-color);
    box-shadow: 0 4px 12px var(--shadow-color);
    margin-bottom: 1.5rem;
}
.material-title {
    font-size: 1.8rem; 
    font-weight: 700; 
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}
.material-text {
    font-size: 1.0rem; 
    line-height: 1.6;
    color: var(--text-color);
}
.material-button-container {
    margin-top: 1rem;
}
.material-button {
    background-color: var(--primary-color) !important;
    color: white !important;
    padding: 0.6rem 1.2rem !important;
    border: none !important;
    border-radius: 8px !important;
    cursor: pointer !important;
}
</style>
""", unsafe_allow_html=True)

# ===================================
# Header
# ===================================
st.title("📘 工程統計學 Engineering Statistics")

# ===================================
# 說明卡片
# ===================================
st.markdown("""
<div class="material-card">
    <div class="material-title">🎯 課程導覽</div>
    <div class="material-text">
        歡迎來到《工程統計學》互動平台！  
        本系統整合資料分析、機率分布、極值統計、蒙地卡羅模擬，以及自動出題等功能。  
        <br><br>
        📌 <b>採用 Material UI 風格</b>，並支援亮色/暗色主題切換。
    </div>
</div>
""", unsafe_allow_html=True)

# ===================================
# 功能卡片（兩欄）
# ===================================
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="material-card">', unsafe_allow_html=True)
    st.markdown('<div class="material-title">📊 描述統計與資料探索</div>', unsafe_allow_html=True)
    st.markdown('<div class="material-text">平均、變異、標準差、直方圖、箱型圖。支援工程資料探索。</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.page_link("pages/01_描述統計.py", label="前往 ➜")

with col2:
    st.markdown('<div class="material-card">', unsafe_allow_html=True)
    st.markdown('<div class="material-title">📈 機率分布互動模組</div>', unsafe_allow_html=True)
    st.markdown('<div class="material-text">正態、對數正態、Gamma、Poisson 等互動視覺化。</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.page_link("pages/02_機率分布互動.py", label="前往 ➜")

# 第二排
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="material-card">', unsafe_allow_html=True)
    st.markdown('<div class="material-title">🌧️ 工程極值統計（GEV）</div>', unsafe_allow_html=True)
    st.markdown('<div class="material-text">暴雨、洪峰、風速等極端事件的重現期推估。</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.page_link("pages/03_極值與_GEV.py", label="前往 ➜")

with col4:
    st.markdown('<div class="material-card">', unsafe_allow_html=True)
    st.markdown('<div class="material-title">🎲 Monte Carlo 風險模擬</div>', unsafe_allow_html=True)
    st.markdown('<div class="material-text">邊坡、洪水、材料強度的風險模擬。</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.page_link("pages/04_MonteCarlo.py", label="前往 ➜")

# 第三排
col5, col6 = st.columns(2)

with col5:
    st.markdown('<div class="material-card">', unsafe_allow_html=True)
    st.markdown('<div class="material-title">📝 自動出題系統</div>', unsafe_allow_html=True)
    st.markdown('<div class="material-text">自動出題、互動作答、即時批改。</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.page_link("pages/05_自動出題.py", label="前往 ➜")

with col6:
    st.markdown('<div class="material-card">', unsafe_allow_html=True)
    st.markdown('<div class="material-title">🎨 UI 外觀設定</div>', unsafe_allow_html=True)
    st.markdown('<div class="material-text">切換主題、配色、字體大小。</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.page_link("pages/06_UI_外觀設定.py", label="前往 ➜")
