import streamlit as st
from theme import apply_theme, init_theme_state

apply_theme()
init_theme_state()

st.title("🎨 UI 外觀設定（Material Design）")

st.markdown('<div class="material-card">', unsafe_allow_html=True)
st.subheader("🌈 主題切換說明")
st.write("""
請到 **Sidebar 左側** 切換下列主題：

- Material Light  
- Material Dark  
- Engineering Blue  

本頁不再個別控制 UI（統一由 theme.py 管理）
""")
st.markdown('</div>', unsafe_allow_html=True)
