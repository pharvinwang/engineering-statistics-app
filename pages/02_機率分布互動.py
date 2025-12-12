import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
# ============================================
# Material UI Style Injection
# ============================================
st.markdown("""
<style>
.material-card {
    background-color: var(--background-color);
    padding: 1.6rem;
    border-radius: 12px;
    border: 1px solid var(--primary-color);
    box-shadow: 0 4px 10px var(--shadow-color);
    margin-bottom: 1.5rem;
}
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
.material-badge {
    display: inline-block;
    padding: 4px 10px;
    background-color: var(--primary-color);
    color: white;
    border-radius: 6px;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)


# ===================================
# 標題與章節說明
# ===================================
st.title("📈 機率分布互動模組")

st.markdown("""
<div class="material-title">🎯 **本章目標與工程用途**</div>


本章主要目標：
- 了解常用工程分布（正態、對數正態、指數、Gamma、Poisson）的特性
- 透過互動式操作調整分布參數，觀察 PDF、CDF、超越機率
- 將統計分布應用於工程風險評估與設計

工程用途示例：
- 水文設計：降雨量、洪峰流量
- 結構設計：材料強度、載重分布
- 土木工程風險評估：邊坡穩定、洪水概率
""")

st.markdown("""
📚 **名詞定義與說明**
- **PDF (Probability Density Function)**：連續型隨機變數的機率密度函數，用於描述特定值附近的相對可能性。
- **CDF (Cumulative Distribution Function)**：累積機率函數，表示隨機變數 ≤ 某值的機率。
- **超越機率 (Exceedance Probability)**：事件大於某臨界值的機率，例如洪水超過設計水位的機率。
- **λ (rate / mean)**：指數分布或 Poisson 分布的參數，決定事件發生頻率。
- **μ, σ**：平均值與標準差，用於正態分布描述資料中心與散布。
""")

st.markdown("---")
st.markdown("### 📌 以下開始互動式操作")

# ===================================
# 互動操作
# ===================================
dist = st.selectbox("選擇分布", ["Normal","Lognormal","Exponential","Gamma","Poisson"])
x_min = st.number_input("x min", value=0.0)
x_max = st.number_input("x max", value=200.0)
x = np.linspace(x_min, x_max, 500)

if dist=="Normal":
    mu = st.slider("μ (mean)", -50.0, 300.0, 100.0)
    sigma = st.slider("σ (std)", 0.1, 200.0, 20.0)
    pdf = stats.norm.pdf(x, loc=mu, scale=sigma)
    cdf = stats.norm.cdf(x, loc=mu, scale=sigma)
elif dist=="Lognormal":
    s = st.slider("shape (s)", 0.1, 2.0, 0.6)
    scale = st.slider("scale (exp(μ))", 1.0, 200.0, 100.0)
    pdf = stats.lognorm.pdf(x, s=s, scale=scale)
    cdf = stats.lognorm.cdf(x, s=s, scale=scale)
elif dist=="Exponential":
    lam = st.slider("λ (rate)", 0.01, 2.0, 0.1)
    pdf = stats.expon.pdf(x, scale=1/lam)
    cdf = stats.expon.cdf(x, scale=1/lam)
elif dist=="Gamma":
    a = st.slider("shape (k)", 0.1, 10.0, 2.0)
    scale = st.slider("scale (θ)", 0.1, 50.0, 10.0)
    pdf = stats.gamma.pdf(x, a, scale=scale)
    cdf = stats.gamma.cdf(x, a, scale=scale)
else: # Poisson discrete
    lam = st.slider("λ (mean)", 0.1, 50.0, 5.0)
    xs = np.arange(int(x_min), int(x_max)+1)
    pmf = stats.poisson.pmf(xs, mu=lam)
    fig, ax = plt.subplots()
    ax.bar(xs, pmf)
    ax.set_title("Poisson PMF")
    st.pyplot(fig)
    st.stop()

fig, ax = plt.subplots(1,2, figsize=(12,4))
ax[0].plot(x, pdf); ax[0].set_title("PDF")
ax[1].plot(x, cdf); ax[1].set_title("CDF")
st.pyplot(fig)

# compute exceedance probability
a = st.number_input("計算 P(X ≥ a) 的 a 值", value=float(x_max))
if dist!="Poisson":
    if dist=="Normal":
        p_exceed = 1 - stats.norm.cdf(a, loc=mu, scale=sigma)
    elif dist=="Lognormal":
        p_exceed = 1 - stats.lognorm.cdf(a, s=s, scale=scale)
    elif dist=="Exponential":
        p_exceed = 1 - stats.expon.cdf(a, scale=1/lam)
    elif dist=="Gamma":
        p_exceed = 1 - stats.gamma.cdf(a, a, scale=scale)
    st.write(f"P(X ≥ {a}) ≈ {p_exceed:.6f} ({p_exceed*100:.4f}%)")
    years = st.slider("累積年數（計算至少一次發生的機率）", 1, 100, 10)
    p_any = 1 - (1-p_exceed)**years
    st.write(f"{years} 年內至少一次發生的機率 ≈ {p_any*100:.4f}%")
