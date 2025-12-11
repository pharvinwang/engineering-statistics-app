import streamlit as st

st.set_page_config(page_title="UI 外觀設定", layout="wide")
st.title("🎨 UI 外觀設定（Theme / Layout / Style）")

st.markdown("""
你可以在這裡調整整個 App 的視覺呈現，包括：

- 主題色（工程藍 / 深色 / 教學亮色）
- 版面 layout（wide / centered）
- 字體大小
- 背景色 / 卡片色（以 CSS 注入）

> 設定會立即影響本頁，但重新整理後會恢復為預設 Streamlit 樣式。
> 若要變成真正的固定主題，需要我協助你放入 `.streamlit/config.toml`。
""")

# --- Theme Options ---
st.subheader("🎨 主題配色")
theme = st.selectbox(
    "選擇主題：",
    ["工程藍", "深色模式", "教學亮色", "原始 Streamlit"]
)

# --- Layout Options ---
st.subheader("📐 頁面版面")
layout = st.radio(
    "選擇頁面寬度：",
    ["寬版（wide）", "固定寬度（centered）"]
)

# --- Font Size ---
st.subheader("🔠 字體大小")
fon
