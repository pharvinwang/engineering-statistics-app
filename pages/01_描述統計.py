import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

st.title("描述統計與視覺化")
st.markdown("上傳 CSV 或使用範例資料。選擇數值欄位後可以查看統計摘要、直方圖、箱型圖、QQ-plot、以及 1.5*IQR 異常值偵測。")

uploaded = st.file_uploader("上傳 CSV (含 header)", type=["csv"])
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

st.write("### 資料預覽")
st.dataframe(df.head())

numeric = df.select_dtypes(include=[np.number]).columns.tolist()
if not numeric:
    st.error("找不到數值欄位。")
    st.stop()

col = st.selectbox("選擇數值欄位", numeric)
data = df[col].dropna().astype(float)

st.write("**統計摘要**")
st.write(data.describe().to_frame().T)

mean = data.mean(); s = data.std(ddof=1); cv = s/mean if mean!=0 else np.nan
st.metric("平均 (mean)", f"{mean:.3f}")
st.metric("樣本標準差 (s)", f"{s:.3f}")
st.metric("變異係數 (CV)", f"{cv:.3f}")

# Outliers 1.5 IQR
q1 = data.quantile(0.25); q3 = data.quantile(0.75); iqr = q3 - q1
lower = q1 - 1.5*iqr; upper = q3 + 1.5*iqr
out_mask = (data < lower) | (data > upper)
st.write(f"IQR={iqr:.3f}, 下界={lower:.3f}, 上界={upper:.3f}，偵測到 {out_mask.sum()} 個異常值。")

# Plots
fig, axes = plt.subplots(1,3, figsize=(15,4))
axes[0].hist(data, bins=8)
axes[0].set_title("Histogram")
axes[1].boxplot(data, vert=False)
axes[1].set_title("Boxplot")
import scipy.stats as stats
res = stats.probplot(data, dist="norm", plot=axes[2])
axes[2].set_title("QQ-plot")
st.pyplot(fig)

st.write("### 異常值列表")
if out_mask.any():
    out_df = df.loc[out_mask.index[out_mask], df.columns]
    st.dataframe(out_df)
else:
    st.write("未偵測到異常值 (1.5*IQR)。")

# Download cleaned with flag
df2 = df.copy()
df2['is_outlier_1.5IQR'] = out_mask.values
csv = df2.to_csv(index=False).encode('utf-8')
st.download_button("下載帶異常值標記的 CSV", csv, file_name="data_with_outlier_flag.csv", mime="text/csv")
