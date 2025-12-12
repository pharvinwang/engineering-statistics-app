import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# -----------------------------
# Material UI Style (CSS)
# -----------------------------
st.markdown("""
<style>
.card {
    background: #ffffffcc;
    padding: 1.2rem 1.4rem;
    border-radius: 12px;
    border: 1px solid #e0e0e0;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 6px #00000015;
}

/* 標題 */
h1, h2, h3 {
    color: #1976d2;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------
st.title("📐 機率分布互動模組（Material UI 版）")
st.markdown("""
此頁讓你可以 **即時切換分布**、**調整參數**、**觀察 PDF / CDF**，  
並計算 **超越機率 P(X ≥ a)** 以及 **N 年內至少一次發生機率**。

支援：
- Normal
- Lognormal
- Exponential
- Gamma
- Poisson（離散）
""")

# -----------------------------
# 選擇分布
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("1️⃣ 選擇機率分布")

dist = st.selectbox("選擇分布", 
    ["Normal", "Lognormal", "Exponential", "Gamma", "Poisson"]
)

x_min = st.number_input("x min", value=0.0)
x_max = st.number_input("x max", value=200.0)

x = np.linspace(x_min, x_max, 500)
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# 分布參數區塊
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("2️⃣ 調整參數")

if dist == "Normal":
    mu = st.slider("μ (平均)", -50.0, 300.0, 100.0)
    sigma = st.slider("σ (標準差)", 0.1, 200.0, 20.0)
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

else:   # Poisson — special case (PMF)
    lam = st.slider("λ (平均)", 0.1, 50.0, 5.0)
    xs = np.arange(int(x_min), int(x_max)+1)
    pmf = stats.poisson.pmf(xs, mu=lam)

    # plot Poisson PMF
    fig, ax = plt.subplots()
    ax.bar(xs, pmf)
    ax.set_title("Poisson PMF")
    st.pyplot(fig)

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# 圖形區塊
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("3️⃣ PDF / CDF 圖形")

fig, ax = plt.subplots(1, 2, figsize=(12, 4))
ax[0].plot(x, pdf)
ax[0].set_title("PDF")
ax[1].plot(x, cdf)
ax[1].set_title("CDF")
st.pyplot(fig)

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# 超越機率區塊
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("4️⃣ 計算超越機率")

a = st.number_input("計算 P(X ≥ a) 的 a 值", value=float(x_max))

if dist == "Normal":
    p_exceed = 1 - stats.norm.cdf(a, loc=mu, scale=sigma)
elif dist == "Lognormal":
    p_exceed = 1 - stats.lognorm.cdf(a, s=s, scale=scale)
elif dist == "Exponential":
    p_exceed = 1 - stats.expon.cdf(a, scale=1/lam)
elif dist == "Gamma":
    p_exceed = 1 - stats.gamma.cdf(a, a, scale=scale)

st.write(f"**P(X ≥ {a}) ≈ {p_exceed:.6f}** （{p_exceed*100:.4f}%）")

years = st.slider("累積年數（計算至少一次發生的機率）", 1, 100, 10)
p_any = 1 - (1 - p_exceed) ** years

st.success(f"➡ **{years} 年內至少一次發生的機率 ≈ {p_any*100:.4f}%**")

st.markdown("</div>", unsafe_allow_html=True)
