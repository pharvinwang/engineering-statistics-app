import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import genextreme as gev
from io import StringIO
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

st.set_page_config(page_title="極值與 GEV", layout="wide")

st.title("🌧️ 極值統計（GEV）")

# ============================================================
# 📘 本章目標與工程用途
# ============================================================
st.markdown("""
<div class="material-title">📘 本章目標與工程用途</div>

本章介紹「極值統計」，用於分析資料中的**最大值行為**，例如：

- 年最大日雨量（Annual Maximum Daily Rainfall）  
- 年最大洪峰流量  
- 年最大風速 / 波浪高度  
- 邊坡土壤強度中最弱位置  
- 材料破壞的極端負載  

工程師可以利用 GEV（Generalized Extreme Value Distribution）估計：

- ⚠️ **某極端事件的重現期（Return Period）是多少？**  
- ⚠️ **超越某強度的機率是多少？**  
- ⚠️ **未來 10 年是否可能發生比歷史更大的事件？**

極值統計特別重要於「工程安全係數」與「設計標準（如百年洪水）」制定。
""", unsafe_allow_html=True)

# ============================================================
# 📚 名詞定義與說明
# ============================================================
st.markdown("""
<div class="material-title">📚 名詞定義與說明</div>

**GEV 分布（Generalized Extreme Value）**  
集合三種極值型態（Gumbel、Fréchet、Weibull）的統一模型。
GEV 有三個參數：

- **位置參數 μ（Location）**：極值大小的中心  
- **尺度參數 σ（Scale）**：極值波動程度  
- **形狀參數 ξ（Shape）**：決定分布尾端形狀  

參數 ξ 的物理意義：  
- ξ = 0：Gumbel（常用於暴雨、風速）  
- ξ > 0：Fréchet（重尾 → 極端更可能，像洪水）  
- ξ < 0：Weibull（有限上界 → 強度上限，如材料強度）  

**超越機率 P(X > x)**  
事件超過某水準 x 的機率，用於評估風險。

**重現期 T**  
T = 1 / P(X > x)  
代表平均多少年會出現一次。

示例：  
T = 100 → 百年洪水  
T = 50 → 五十年暴雨  
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""<div class="material-title">🧪 互動式操作</div>""", unsafe_allow_html=True)

# ============================================================
# 🧪 互動式操作
# ============================================================

# --- Data input selection ---
uploaded = st.file_uploader("上傳 CSV（含 header）", type=["csv"])
use_sample = st.checkbox("使用範例資料（年最大日雨量 20 筆）", value=True)

# Sample dataset
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

if use_sample:
    df = pd.read_csv(StringIO(sample))
else:
    if uploaded is None:
        st.info("請上傳 CSV 或使用範例資料")
        st.stop()
    df = pd.read_csv(uploaded)

st.write("### 📄 資料預覽")
st.dataframe(df.head())

# Select numeric column
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
col = st.selectbox("選擇要做極值分析的欄位", numeric_cols)

data = df[col].astype(float)

# Fit GEV
ξ, μ, σ = gev.fit(-data)  # SciPy 以負號做最大值
ξ = -ξ  # 修正符號（讓 ξ 與教科書一致）

st.write("### 📌 估計後的 GEV 參數")
st.write(f"位置參數 μ = **{μ:.3f}**")
st.write(f"尺度參數 σ = **{σ:.3f}**")
st.write(f"形狀參數 ξ = **{ξ:.3f}**")

# Input x for exceedance probability
x = st.slider("選擇欲估計的極端事件大小（如雨量 mm）", 
              float(data.min()), 
              float(data.max() * 2), 
              float(data.mean()))

prob = 1 - gev.cdf(-x, -ξ, μ, σ)
T = 1/prob if prob > 0 else np.inf

st.write(f"超越機率 P(X > {x:.1f}) = **{prob:.4f}**")
st.write(f"對應重現期 T = **{T:.1f} 年**")

# Plot
xs = np.linspace(min(data)*0.9, max(data)*1.2, 200)
ys = 1 - gev.cdf(-xs, -ξ, μ, σ)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(xs, ys)
ax.axvline(x, color='r', linestyle='--')
ax.set_title("GEV 超越機率曲線")
ax.set_xlabel(col)
ax.set_ylabel("P(X > x)")
st.pyplot(fig)

# Download parameters
param_df = pd.DataFrame({"mu":[μ], "sigma":[σ], "xi":[ξ]})
csv = param_df.to_csv(index=False).encode("utf-8")

st.download_button("下載 GEV 參數 CSV", csv, file_name="GEV_params.csv")
