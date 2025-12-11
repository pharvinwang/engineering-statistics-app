import streamlit as st

# ------------------------------------------------------
# 儲存主題設定
# ------------------------------------------------------
def init_theme_state():
    if "theme" not in st.session_state:
        st.session_state.theme = "Material Light"


# ------------------------------------------------------
# Material UI 主題 CSS
# ------------------------------------------------------
def get_material_theme_css(theme_name):

    # ===== Material Light =====
    if theme_name == "Material Light":
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif !important;
            background-color: #FAFAFA !important;
            color: #212121 !important;
        }

        h1, h2, h3 {
            color: #1A237E !important;
            font-weight: 500 !important;
        }

        .material-card {
            background: #FFFFFF;
            padding: 1.4rem;
            border-radius: 12px;
            box-shadow: 0px 3px 8px rgba(0,0,0,0.12);
        }

        .stButton>button {
            background-color: #2962FF !important;
            color: white !important;
            border-radius: 6px !important;
            border: none;
            padding: 0.6rem 1.2rem !important;
            font-weight: 500 !important;
        }

        section[data-testid="stSidebar"] {
            background-color: #ECEFF1 !important;
        }
        </style>
        """

    # ===== Material Dark =====
    elif theme_name == "Material Dark":
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif !important;
            background-color: #121212 !important;
            color: #E0E0E0 !important;
        }

        h1, h2, h3 {
            color: #90CA
