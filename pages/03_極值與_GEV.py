import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import scipy.stats as stats
import matplotlib.pyplot as plt

st.title("極值分析 (Gumbel / GEV 示範)")
st.markdown("上傳年度極值（每年一筆）。此頁面提供簡易 L-moment (用 scipy fit) 與 Gumbel 快速估計示範。")

uploaded = st.file_uploader("上傳 CSV（含年度極值）", type=["csv"])
use_sample = st.checkbox("使用範例資料 (20 年年最大日雨量)", value=True)

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
        st.info("請上傳 CSV 或勾選使用範例資料。")
        st.stop()
    df = pd.read_csv(uploaded)

st.dataframe(df.head())

numeric = df.select_dtypes(include=[np.number]).columns.tolist()
col = st.selectbox("選擇年極值欄位", numeric)
data = df[col].dropna().astype(float)

# quick Gumbel using mean/std
mean = data.mean(); s = data.std(ddof=1)
beta = s / (np.pi/np.sqrt(6))
gamma = 0.5772156649
mu = mean - gamma*beta

st.write(f"樣本平均={mean:.3f}, 樣本 s={s:.3f}")
st.write(f"Gumbel quick-estimate: μ={mu:.3f}, β={beta:.3f}")

x_val = st.number_input("計算 P(X ≥ x) 的 x 值", value=float(data.max()))
z = (x_val - mu)/beta
Fx = np.exp(-np.exp(-z))
p_exceed = 1 - Fx
st.write(f"P(X ≥ {x_val}) ≈ {p_exceed*100:.4f}% 每年")

years = st.slider("累積年數", 1, 100, 10)
p_any = 1 - (1-p_exceed)**years
st.write(f"{years} 年內至少一次發生機率 ≈ {p_any*100:.4f}%")

# plot empirical vs fitted
x = np.linspace(min(data)*0.8, max(data)*1.4, 200)
cdf_gumbel = np.exp(-np.exp(-(x-mu)/beta))
plt.figure(figsize=(8,4))
plt.plot(np.sort(data), np.arange(1, len(data)+1)/ (len(data)+1), marker='o', linestyle='none', label='Empirical')
plt.plot(x, cdf_gumbel, label='Gumbel CDF')
plt.xlabel(col)
plt.ylabel('Cumulative Probability')
plt.legend()
st.pyplot(plt)
