import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO
import scipy.stats as stats

st.set_page_config(page_title="描述統計", layout="wide")

st.title("📊 描述統計與資料探索")

# -------------------------------------------
# 📘 本章目標與工程用途
# -------------------------------------------
st.markdown("""
<div class="material-title">📘 本章目標與工程用途</div>

本章的目的在於快速檢視資料的「集中程度」與「離散程度」，並透過可視化方式
協助工程師理解資料是否具有異常、偏態、長尾行為。

工程用途示例：
- 材料強度（如混凝土抗壓強度）是否穩定？
- 年最大日雨量是否逐年變大？
- 風速、流量等工程環境條件是否出現極端值？
""", unsafe_allow_html=True)

# -------------------------------------------
# 📚 名詞定義與說明
# -------------------------------------------
st.markdown("""
<div class="material-title">📚 名詞定義與說明</div>

**平均值 (Mean)**：資料的集中位置。  
**標準差 (Standard Deviation)**：資料的離散程度。  
**變異係數 (CV)**：衡量「資料相對變異程度」，工程上常用來評估材料穩定性。  
**IQR (四分位距)**：Q3 − Q1，用於偵測異常值。  
**1.5 × IQR 異常值**：落在下界或上界以外的資料視為異常點。  

工程用途：
- 判斷設備量測是否異常  
- 偵測材料瑕疵  
- 篩除有問題的感測器資料  
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""<div class="material-title">🧪 互動式操作</div>""", unsafe_allow_html=True)

# -------------------------------------------
# 🧪 互動式操作
# -------------------------------------------

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
        st.info("請上傳 CSV 或勾選使用範例資料")
        st.stop()
    df = pd.read_csv(uploaded)

st.write("### 📄 資料預覽")
st.dataframe(df.head())

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if not numeric_cols:
    st.error("❌ 找不到數值欄位")
    st.stop()

col = st.selectbox("選擇數值欄位", numeric_cols)
data = df[col].dropna().astype(float)

st.write("### 📌 統計摘要")
st.write(data.describe().to_frame().T)

mean = data.mean()
s = data.std(ddof=1)
cv = s/mean if mean!=0 else np.nan

st.metric("平均 (Mean)", f"{mean:.3f}")
st.metric("標準差 (Std)", f"{s:.3f}")
st.metric("變異係數 (CV)", f"{cv:.3f}")

# 1.5*IQR Outlier detection
q1 = data.quantile(0.25)
q3 = data.quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
mask = (data < lower) | (data > upper)

st.write(f"IQR = **{iqr:.3f}**, 下界 = **{lower:.3f}**, 上界 = **{upper:.3f}**")
st.write(f"🔍 偵測到 **{mask.sum()}** 個異常值")

fig, ax = plt.subplots(1, 3, figsize=(15, 4))
ax[0].hist(data, bins=8); ax[0].set_title("Histogram")
ax[1].boxplot(data, vert=False); ax[1].set_title("Boxplot")
stats.probplot(data, dist="norm", plot=ax[2])
ax[2].set_title("QQ-Plot")
st.pyplot(fig)

st.write("### 📦  異常值列表")
if mask.any():
    st.dataframe(df.loc[mask])
else:
    st.write("未偵測到異常值")

# Export
df2 = df.copy()
df2["is_outlier_1.5IQR"] = mask.values
csv = df2.to_csv(index=False).encode("utf-8")

st.download_button("下載含異常值標記 CSV", csv, file_name="with_outliers.csv")
