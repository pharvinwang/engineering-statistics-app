import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from theme import apply_theme
apply_theme()

st.title("📊 描述統計（Descriptive Statistics）")

st.markdown('<div class="material-card">', unsafe_allow_html=True)
st.subheader("📘 上傳或輸入你的資料")

data_input = st.text_area(
    "請以逗號或換行分隔資料：",
    "12, 14, 11, 15, 13"
)

if st.button("計算統計量"):
    try:
        data = np.array([float(x) for x in data_input.replace("\n", ",").split(",") if x.strip() != ""])
        
        mean_val = data.mean()
        std_val = data.std(ddof=1)
        cv_val = std_val / mean_val

        st.success("計算成功！")

        st.markdown('<div class="material-card">', unsafe_allow_html=True)
        st.subheader("📌 統計量結果")
        st.write(f"平均值 (Mean)：**{mean_val:.3f}**")
        st.write(f"標準差 (Std)：**{std_val:.3f}**")
        st.write(f"變異係數 CV：**{cv_val:.3f}**")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="material-card">', unsafe_allow_html=True)
        st.subheader("📈 直方圖")
        fig, ax = plt.subplots()
        ax.hist(data, bins=5)
        ax.set_title("Histogram")
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"資料格式錯誤：{e}")

st.markdown('</div>', unsafe_allow_html=True)
