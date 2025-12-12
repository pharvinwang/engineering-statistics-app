import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from io import StringIO

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

# ============================================
# Page Title
# ============================================
st.title("🌧️ 工程極值分析（Gumbel / GEV）")

st.markdown("""
<div class="material-card">
    <div class="material-title">📘 本章目標與工程用途</div>
    <div class="material-text">
        工程設計常需要估計「極端事件」的發生機率，例如：  
        - 暴雨的最大日雨量（排水 / 沖刷）  
        - 洪峰流量（堤防 / 大壩安全）  
        - 最大風速（高樓 / 橋梁抗風）  
        - 最大全浪（海堤 / 離岸平台）  

        本頁示範：  
        1. 極值資料上傳與檢視  
        2. 使用 **Gumbel 分布** 快速估計重現期  
        3. 計算超越機率與年發生機率  
        4. 實證 CDF vs. Gumbel 理論 CDF 比較  

        這些分析方法在工程界用於：  
        <span class="material-badge">設計標準推估</span>
        <span class="material-badge">風險評估</span>
        <span class="material-badge">重現期分析</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# 名詞定義卡片
# ============================================
st.markdown("""
<div class="material-card">
    <div class="material-title">📚 名詞定義：GEV、Gumbel、重現期</div>
    <div class="material-text">

**📌 年最大值 (Annual Maxima)**  
每年挑出「最大的」那一筆數據，如最大日雨量、最大風速。

**📌 Gumbel 分布 (Extreme Type I)**  
GEV 的一種特例，用來描述極端事件的最大值。簡化公式、容易估參。

**📌 GEV 分布 (Generalized Extreme Value)**  
更廣泛的極值分布，包含三類型（Fréchet、Weibull、Gumbel）。

**📌 重現期 (Return Period)**  
平均多久會出現一次某個極端事件，例如：  
T = 50 年 → 平均 50 年出現一次  
對應超越機率：p = 1/T。

**📌 超越機率 (Exceedance Probability)**  
事件一年內大於某閾值 x 的機率：  
p = P(X ≥ x)

</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# Upload Section
# ============================================
st.header("📁 輸入極值資料（每年一筆）")

uploaded = st.file_uploader("上傳 CSV（需含年度極值欄位）", type=["csv"])
use_sample = st.checkbox("使用範例（20 年最大日雨量）", value=True)

if use_sample:
    sample = """year,max_daily_rain_mm
2001,67
2002,98
2003,103
2004,84
2005,112
2006,135
2007,156
2008,90
2009,87
2010,120
2011,140
2012,155
2013,130
2014,160
2015,164
2016,142
2017,110
2018,97
2019,85
2020,81
"""
    df = pd.read_csv(StringIO(sample))
else:
    if uploaded is None:
        st.info("請上傳 CSV 或使用範例資料。")
        st.stop()
    df = pd.read_csv(uploaded)

st.dataframe(df.head())

numeric = df.select_dtypes(include=[np.number]).columns.tolist()
col = st.selectbox("選擇「年度極值」欄位", numeric)

data = df[col].dropna().astype(float)

# ============================================
# Gumbel Quick Estimate
# ============================================
st.header("📌 Gumbel 分布快速參數估計")

mean = data.mean()
s = data.std(ddof=1)
beta = s / (np.pi / np.sqrt(6))
gamma = 0.5772156649
mu = mean - gamma * beta

st.markdown(f"""
<div class="material-card">
<div class="material-title">📐 Gumbel 快速估計結果</div>
<div class="material-text">
平均 = {mean:.3f}  
樣本標準差 = {s:.3f}  
<br>
**估計參數：**  
μ = {mu:.3f}  
β = {beta:.3f}  
</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# Exceedance Probability
# ============================================
st.header("🎯 計算超越機率與重現期")

x_val = st.number_input("輸入要估計超越機率的極值 x", value=float(data.max()))

z = (x_val - mu) / beta
Fx = np.exp(-np.exp(-z))
p_exceed = 1 - Fx

st.success(f"P(X ≥ {x_val}) ≈ {p_exceed:.4f}  （年超越機率）")

T = 1 / p_exceed if p_exceed > 0 else np.inf
st.info(f"對應的重現期 ≈ **{T:.2f} 年**")

years = st.slider("計算 N 年內至少一次發生的機率", 1, 100, 10)
p_any = 1 - (1 - p_exceed)**years
st.write(f"{years} 年內至少一次發生機率：**{p_any:.2%}**")

# ============================================
# Plot
# ============================================
st.header("📉 實證 CDF vs Gumbel 理論 CDF")

x = np.linspace(min(data)*0.8, max(data)*1.4, 200)
cdf_gumbel = np.exp(-np.exp(-(x - mu)/beta))

plt.figure(figsize=(8,4))
plt.plot(np.sort(data), np.arange(1,len(data)+1)/(len(data)+1),
         marker='o', linestyle='none', label="Empirical")
plt.plot(x, cdf_gumbel, label="Gumbel CDF")
plt.xlabel(col)
plt.ylabel("Cumulative Probability")
plt.legend()
st.pyplot(plt)
