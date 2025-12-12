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
.material-subtitle {
    font-size: 1.2rem; 
    color: var(--text-color);
    margin-bottom: 1rem;
}
.material-text {
    font-size: 1.0rem; 
    line-height: 1.6;
    color: var(--text-color);
}
.material-button > button {
    background-color: var(--primary-color) !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.2rem !important;
    border: none !important;
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
        本系統整合資料分析、機率分布、極值統計、蒙地卡羅模擬，以及自動出題等功能，  
        讓你能真正「用統計解工程問題」。
        <br><br>
        📌 <b>所有互動介面皆採 Material UI 設計</b>，並支援主題切換（亮色 / 暗色）。
    </div>
</div>
""", unsafe_allow_html=True)

# ===================================
# 功能卡片（兩欄式）
# ===================================
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="material-card">
        <div class="material-title">📊 描述統計與資料探索</div>
        <div class="material-text">
            查看平均值、變異、標準差、箱型圖、直方圖。<br>
            適用於土壤、混凝土、降雨、材料強度等各類工程資料。
        </div>
        <div class="material-button">
            <a href="/01_描述統計" target="_self">
                <button>前往 ➜</button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="material-card">
        <div class="material-title">📈 機率分布互動模組</div>
        <div class="material-text">
            正態、對數正態、威布爾、指數分布等工程常用分布皆可互動調整。
            查看 PDF、CDF、百分位數、超越機率。
        </div>
        <div class="material-button">
            <a href="/02_機率分布互動" target="_self">
                <button>前往 ➜</button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===================================
# 第二排
# ===================================
col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="material-card">
        <div class="material-title">🌧️ 工程極值統計（GEV）</div>
        <div class="material-text">
            估計暴雨、洪峰流量、風速、波浪等極端事件之重現期與超越機率。
        </div>
        <div class="material-button">
            <a href="/03_極值與GEV" target="_self">
                <button>前往 ➜</button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="material-card">
        <div class="material-title">🎲 蒙地卡羅風險模擬</div>
        <div class="material-text">
            隨機模擬工程事件，如邊坡穩定度、洪水風險、材料不確定性。
        </div>
        <div class="material-button">
            <a href="/04_MonteCarlo_模擬" target="_self">
                <button>前往 ➜</button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===================================
# 第三排
# ===================================
col5, col6 = st.columns(2)

with col5:
    st.markdown("""
    <div class="material-card">
        <div class="material-title">📝 自動出題系統</div>
        <div class="material-text">
            自動產生工程統計題目、互動作答、即時判分，非常適合練習。
        </div>
        <div class="material-button">
            <a href="/05_自動出題系統" target="_self">
                <button>前往 ➜</button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="material-card">
        <div class="material-title">🎨 UI 外觀設定</div>
        <div class="material-text">
            選擇主題顏色、陰影效果、亮暗模式。  
            全站外觀將同步更新。
        </div>
        <div class="material-button">
            <a href="/06_UI外觀設定" target="_self">
                <button>前往 ➜</button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
