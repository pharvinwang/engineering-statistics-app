import streamlit as st

# 初始化 Session State
def init_theme_state():
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "light"

# 全域主題套用
def apply_theme():

    init_theme_state()

    # Sidebar 主題切換選單
    mode = st.sidebar.radio(
        "🎨 Material UI 主題",
        ["Material Light", "Material Dark", "Engineering Blue"],
        index=0
    )

    st.session_state.theme_mode = mode

    # 套用 CSS
    if mode == "Material Light":
        css = MATERIAL_LIGHT
    elif mode == "Material Dark":
        css = MATERIAL_DARK
    else:
        css = ENGINEERING_BLUE

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# ------------------------------------------------------------
#           Material UI Style Sheets
# ------------------------------------------------------------

MATERIAL_LIGHT = """
body {
    background-color: #FAFAFA;
    font-family: 'Roboto', sans-serif;
}
.material-card {
    background: #FFFFFF;
    padding: 20px;
    border-radius: 12px;
    margin: 20px 0px;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
}
"""

MATERIAL_DARK = """
body {
    background-color: #121212;
    color: #EEEEEE;
    font-family: 'Roboto', sans-serif;
}
.material-card {
    background: #1E1E1E;
    padding: 20px;
    border-radius: 12px;
    margin: 20px 0px;
    box-shadow: 0px 2px 8px rgba(255,255,255,0.1);
}
"""

ENGINEERING_BLUE = """
body {
    background-color: #F0F6FF;
    font-family: 'Roboto', sans-serif;
}
.material-card {
    background: #FFFFFF;
    padding: 20px;
    border-radius: 12px;
    border-left: 6px solid #1976D2;
    margin: 20px 0px;
    box-shadow: 0px 2px 6px rgba(25,118,210,0.2);
}
"""
