
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
