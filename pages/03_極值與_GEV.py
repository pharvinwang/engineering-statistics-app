import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gumbel_r

from theme import apply_theme
apply_theme()

st.title("🌧️ 工程極值推估（Gumbel Distribution）")

st.markdown('<div class="material-card">', unsafe_allow_html=True)
st.subheader("📁 上傳或使用示範資料")

uploaded = st.file_uploader("上傳最大日雨量 CSV", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)
else:
    df = pd.DataFrame({"max_rain": [67, 98, 103, 84, 112, 135, 156, 90, 87, 120,
                                   140, 155, 130, 160, 164, 142, 110, 97, 85, 81]})
    st.info("使用預設資料：20 年最大日雨量")

st.dataframe(df)
st.markdown('</div>', unsafe_allow_html=True)

x = df["max_rain"].values

# Fit Gumbel
loc, scale = gumbel_r.fit(x)

st.markdown('<div class="material-card">', unsafe_allow_html=True)
st.subheader("📌 Gumbel 參數")
st.write(f"位置參數 loc = **{loc:.3f}**")
st.write(f"尺度參數 scale = **{scale:.3f}**")
st.markdown('</div>', unsafe_allow_html=True)

# Return level
st.markdown('<div class="material-card">', unsafe_allow_html=True)
st.subheader("⚡ 重現期估計")

T = st.number_input("重現期 T（年）", value=10)
RT = gumbel_r.ppf(1 - 1/T, loc=loc, scale=scale)

st.write(f"**{T} 年重現期降雨： {RT:.2f} mm**")
st.markdown('</div>', unsafe_allow_html=True)
