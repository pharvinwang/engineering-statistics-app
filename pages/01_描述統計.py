import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from io import StringIO
from theme import apply_theme

# 套用 Material UI 主題
apply_theme()

st.set_page_config(page_title="描述統計", page_icon="📊", layout="wide")

# ===============================
# 名詞定義卡片（Material UI）
# ===============================
st.markdown("""
<div class="material-card">
  <div class="material-title">📘 名詞定義與工程應用（Descriptive Statistics）</div>
  <div class="material-text">

  <b>平均值 Mean：</b><br>
  數據的中心位置，用來代表「材料平均強度」、「平均含水量」、「年平均雨量」。  
  <br><br>

  <b>標準差 Standard Deviation：</b><br>
  描述資料的波動程度。工程上用於判斷「材料品質穩定度」或「氣候變異程度」。  
  <u>標準差越小 → 品質越穩定。</u>  
  <br><br>

  <b>變異係數 CV：</b><br>
  CV = 標準差 / 平均值  
  用來比較「不同量級資料」的穩定度，例如：  
  - 兩種不同地區的降雨量  
  - 不同機齡設備的震動強度  
  <br>
  CV 越小代表資料一致性高。  
  <br><br>

  <b>IQR（四分位距）：</b><br>
  介於 Q1~Q3 的區間。  
  工程上用於「偵測異常值」、「品質管制」、「數據清理」。  
  <br>
  異常值範圍 = Q1 - 1.5×IQR 〜 Q3 + 1.5×IQR  
  <br><br>

  （註：後續 *極值統計* 章節將會更深入處理極端事件，例如最大強度、最大日雨量等。）
  </div>
</div>
""", unsafe_allow_html=True)

# ===============================
# 原本功能（保留）
# ===============================
st.title("📊 描述統計與視覺化（EDA）")
st.markdown("上傳 CSV 或使用範例資料，進行統計摘要、異常值分析與視覺化。")

uploaded = st.file_uploader("上傳 CSV (含 header)", type=["csv"])
use_sample = st.checkbox("使用範例資料（20 年年最大日雨量）", value=True)

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

# ===============================
# Data Preview
# ===============================
st.write("### 📄 資料預覽")
st.dataframe(df.head(), use_container_width=True)

numeric = df.select_dtypes(include=[np.number]).columns.tolist()
if not numeric:
    st.error("找不到數值欄位。")
    st.stop()

col = st.selectbox("選擇數值欄位", numeric)
data = df[col].dropna().astype(float)

# ===============================
# 統計摘要
# ===============================
st.write("### 📈 統計摘要")
st.write(data.describe().to_frame().T)

mean = data.mean()
std = data.std(ddof=1)
cv = std / mean if mean != 0 else np.nan

mcol1, mcol2, mcol3 = st.columns(3)
mcol1.metric("平均值 Mean", f"{mean:.3f}")
mcol2.metric("標準差 Std", f"{std:.3f}")
mcol3.metric("變異係數 CV", f"{cv:.3f}")

# ===============================
# IQR Outlier Detection
# ===============================
q1 = data.quantile(0.25)
q3 = data.quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

outliers = (data < lower) | (data > upper)
st.write(f"#### 🛑 IQR 異常值偵測：共 {outliers.sum()} 個")
st.write(f"IQR = {iqr:.3f}，下界 = {lower:.3f}，上界 = {upper:.3f}")

# ===============================
# 圖形
# ===============================
st.write("### 📊 資料視覺化")

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].hist(data, bins=8)
axes[0].set_title("Histogram")

axes[1].boxplot(data, vert=False)
axes[1].set_title("Boxplot")

stats.probplot(data, dist="norm", plot=axes[2])
axes[2].set_title("QQ-plot")

st.pyplot(fig)

# ===============================
# Outlier List
# ===============================
st.write("### 📋 異常值列表")
if outliers.sum() > 0:
    st.dataframe(df.loc[outliers.index[outliers]])
else:
    st.write("未偵測到異常值。")

# ===============================
# Download CSV
# ===============================
df_out = df.copy()
df_out["is_outlier_IQR"] = outliers.values
csv = df_out.to_csv(index=False).encode("utf-8")
st.download_button("下載含異常值標記資料", csv, "data_with_outliers.csv", "text/csv")
