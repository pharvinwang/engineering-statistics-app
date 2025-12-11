import streamlit as st

# ---------------------------------------------------------
# 1. SessionState：儲存目前主題
# ---------------------------------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "Material Light"

# ---------------------------------------------------------
# 2. 主題切換器（放在 Sidebar）
# ---------------------------------------------------------
with st.sidebar:
    st.header("🎨 UI Theme")
    theme = st.selectbox(
        "選擇主題：",
        ["Material Light", "Material Dark", "Engineering Blue"],
        index=["Material Light", "Material Dark", "Engineering Blue"].index(st.session_state.theme)
    )
    st.session_state.theme = theme


# ---------------------------------------------------------
# 3. Material UI CSS 定義
# ---------------------------------------------------------

def get_material_theme_css(theme_name):

    # ------ Material Light ------
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
        }

        section[data-testid="stSidebar"] {
            background-color: #ECEFF1 !important;
        }
        </style>
        """

    # ------ Material Dark ------
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
            color: #90CAF9 !important;
            font-weight: 500 !important;
        }

        .material-card {
            background: #1E1E1E !important;
            padding: 1.4rem;
            border-radius: 12px;
            box-shadow: 0px 3px 8px rgba(0,0,0,0.35);
        }

        .stButton>button {
            background-color: #90CAF9 !important;
            color: #000 !important;
            border-radius: 6px !important;
            border: none;
            padding: 0.6rem 1.2rem !important;
            font-weight: 500 !important;
        }

        section[data-testid="stSidebar"] {
            background-color: #263238 !important;
        }
        </style>
        """

    # ------ 工程藍（Engineering Blue）------
    elif theme_name == "Engineering Blue":
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif !important;
            background-color: #F5F9FF !important;
            color: #0D1B2A !important;
        }

        h1, h2, h3 {
            color: #003f88 !important;
            font-weight: 600 !important;
        }

        .material-card {
            background: #FFFFFF;
            padding: 1.4rem;
            border-radius: 12px;
            box-shadow: 0px 3px 10px rgba(0,84,159,0.15);
            border-left: 6px solid #00509E;
        }

        .stButton>button {
            background-color: #00509E !important;
            color: white !important;
            border-radius: 6px !important;
            border: none;
            padding: 0.6rem 1.2rem !important;
        }

        section[data-testid="stSidebar"] {
            background-color: #E3ECF8 !important;
        }
        </style>
        """

    return ""


# ---------------------------------------------------------
# 4. 注入 CSS
# ---------------------------------------------------------
st.markdown(get_material_theme_css(st.session_state.theme), unsafe_allow_html=True)


# ---------------------------------------------------------
# 5. Home Page 內容
# ---------------------------------------------------------
st.title("📘 工程統計互動學習平台")
st.write(f"目前主題：**{st.session_state.theme}**")
st.write("這是首頁，所有頁面都會自動套用你選擇的 Material UI 主題。")

with st.container():
    st.markdown('<div class="material-card">', unsafe_allow_html=True)
    st.subheader("🚀 歡迎使用工程統計互動平台")
    st.write("左側可切換主題，也可以瀏覽不同學習內容。")
    st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
st.set_page_config(page_title="工程統計互動平台", layout="wide")
st.title("工程統計互動平台（多頁版）")
st.markdown("""
歡迎使用 *Engineering Statistics Interactive Platform*  
左側選單包含各章節模組：  
- **描述統計**（統計摘要、視覺化、異常值偵測）  
- **機率分布互動**（正態、指數、對數常態等）  
- **極值與 GEV**（年極值分析、return period）  
- **Monte Carlo 風險模擬**（簡易結構可靠度）  
- **自動出題與批改**（教師用）  

此平台設計為教學用途。若要用於正式工程設計，請採用嚴謹的參數估計與不確定性分析流程。
""")
st.sidebar.success("從左側選單選擇章節開始。")
st.write("範例資料（20 年年最大日雨量）已放在 `sample_rainfall_max20.csv`，你亦可上傳自己的 CSV。")
