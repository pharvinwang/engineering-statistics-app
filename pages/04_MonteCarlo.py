import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from theme import apply_theme
apply_theme()

st.title("🎯 Monte Carlo 風險模擬")

st.markdown('<div class="material-card">', unsafe_allow_html=True)
st.subheader("🔧 參數設定")

mu = st.number_input("平均值 μ", value=10.0)
sigma = st.number_input("標準差 σ", value=2.0)
limit = st.number_input("失效門檻值", value=15.0)
N = st.number_input("模擬次數 N", value=5000, step=1000)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="material-card">', unsafe_allow_html=True)
if st.button("開始模擬"):
    samples = np.random.normal(mu, sigma, int(N))
    pf = np.mean(samples > limit)

    st.subheader("📌 結果")
    st.write(f"失效機率 Pf = **{pf:.4f}**")

    fig, ax = plt.subplots()
    ax.hist(samples, bins=30)
    ax.axvline(limit, color="red")
    ax.set_title("Monte Carlo Samples")
    st.pyplot(fig)

st.markdown('</div>', unsafe_allow_html=True)
