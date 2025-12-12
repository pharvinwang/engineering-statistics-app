import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, expon, uniform

from theme import apply_theme
apply_theme()

st.title("🎲 機率分布互動模組")

dist_type = st.selectbox("選擇分布種類：", ["Normal", "Exponential", "Uniform"])

st.markdown('<div class="material-card">', unsafe_allow_html=True)
st.subheader("🔧 分布參數設定")

if dist_type == "Normal":
    mu = st.number_input("平均 (mu)", value=0.0)
    sigma = st.number_input("標準差 (sigma)", value=1.0)
    dist = norm(mu, sigma)

elif dist_type == "Exponential":
    lam = st.number_input("λ（rate）", value=1.0)
    dist = expon(scale=1/lam)

else:
    a = st.number_input("最小值 a", value=0.0)
    b = st.number_input("最大值 b", value=1.0)
    dist = uniform(a, b - a)

x = np.linspace(-5, 5, 300)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="material-card">', unsafe_allow_html=True)
st.subheader("📈 PDF 曲線")

fig, ax = plt.subplots()
ax.plot(x, dist.pdf(x))
ax.set_title("Probability Density Function")
st.pyplot(fig)
st.markdown('</div>', unsafe_allow_html=True)
