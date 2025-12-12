import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


st.set_page_config(page_title="機率分布互動", layout="wide")

# ============================================
# Material UI Style Injection
# ============================================
st.markdown("""
<style>
.material-title {
    font-size: 1.6rem; 
    font-weight: 700; 
    color: var(--primary-color);
    margin-bottom: 0.3rem;
}
.material-text {
    font-size: 1.05rem; 
    line-height: 1.6;
    color: var(--text-color);
}
</style>
""", unsafe_allow_html=True)

# ===================================
# Title
# ===================================
st.title("📈 機率分布互動模組")

# ===================================
# Section 1: 本章目標與工程用途
# ===================================
st.markdown("""
<div class="material-title">📘 本章目標與工程用途</div>

本章主要目標：

- 認識工程中常見的機率分布模型（正態、對數正態、指數、Gamma、Poisson）
- 透過互動操作調整參數，以理解資料分布行為
- 學習如何使用 PDF、CDF、超越機率評估風險

工程用途示例：

- 洪水風險曲線推估  
- 材料強度不確定性分析  
- 設計安全係數評估  

""", unsafe_allow_html=True)

# ===================================
# Section 2: 名詞定義
# ===================================
st.markdown("""
<div class="material-title">📚 名詞定義與說明</div>

- **PDF（機率密度函數）**：描述連續變數落在某區間的相對可能性  
- **CDF（累積機率函數）**：事件小於等於某值的機率  
- **超越機率（Exceedance Probability）**：事件「大於某值」的機率，常用於工程風險判斷  
- **分布參數**：如 μ、σ、shape、scale，決定資料的變化形態  

""", unsafe_allow_html=True)

# 分隔線
st.markdown("---")
st.markdown("""<div class="material-title">🧪 互動式操作</div>""", unsafe_allow_html=True)

# ===================================
# Interactive module
# ===================================

dist = st.selectbox("選擇分布模型", 
                    ["Normal", "Lognormal", "Exponential", "Gamma", "Poisson"])

x_min = st.number_input("x min", value=0.0)
x_max = st.number_input("x max", value=200.0)
x = np.linspace(x_min, x_max, 500)

if dist == "Normal":
    mu = st.slider("μ (mean)", -50.0, 300.0, 100.0)
    sigma = st.slider("σ (std)", 0.1, 200.0, 20.0)
    pdf = stats.norm.pdf(x, loc=mu, scale=sigma)
    cdf = stats.norm.cdf(x, loc=mu, scale=sigma)

elif dist == "Lognormal":
    s = st.slider("shape (s)", 0.1, 2.0, 0.6)
    scale = st.slider("scale (exp(μ))", 1.0, 200.0, 100.0)
    pdf = stats.lognorm.pdf(x, s=s, scale=scale)
    cdf = stats.lognorm.cdf(x, s=s, scale=scale)

elif dist == "Exponential":
    lam = st.slider("λ (rate)", 0.01, 2.0, 0.1)
    pdf = stats.expon.pdf(x, scale=1/lam)
    cdf = stats.expon.cdf(x, scale=1/lam)

elif dist == "Gamma":
    a = st.slider("shape (k)", 0.1, 10.0, 2.0)
    scale = st.slider("scale (θ)", 0.1, 50.0, 10.0)
    pdf = stats.gamma.pdf(x, a, scale=scale)
    cdf = stats.gamma.cdf(x, a, scale=scale)

else:  # Poisson
    lam = st.slider("λ (mean)", 0.1, 50.0, 5.0)
    xs = np.arange(int(x_min), int(x_max) + 1)
    pmf = stats.poisson.pmf(xs, mu=lam)
    fig, ax = plt.subplots()
    ax.bar(xs, pmf)
    ax.set_title("Poisson PMF")
    st.pyplot(fig)
    st.stop()

fig, ax = plt.subplots(1, 2, figsize=(12, 4))
ax[0].plot(x, pdf); ax[0].set_title("PDF")
ax[1].plot(x, cdf); ax[1].set_title("CDF")
st.pyplot(fig)

a = st.number_input("計算 P(X ≥ a) 的 a 值", value=float(x_max))

if dist != "Poisson":
    if dist == "Normal": p_exceed = 1 - stats.norm.cdf(a, mu, sigma)
    elif dist == "Lognormal": p_exceed = 1 - stats.lognorm.cdf(a, s=s, scale=scale)
    elif dist == "Exponential": p_exceed = 1 - stats.expon.cdf(a, scale=1/lam)
    elif dist == "Gamma": p_exceed = 1 - stats.gamma.cdf(a, a, scale=scale)

    st.write(f"📌 **超越機率** P(X ≥ {a}) = **{p_exceed:.4f}**")

    years = st.slider("累積年數（計算至少一次發生的機率）", 1, 100, 10)
    p_any = 1 - (1 - p_exceed)**years
    st.write(f"⛈️ **{years} 年內至少一次發生的機率** ＝ {p_any*100:.3f}%")
