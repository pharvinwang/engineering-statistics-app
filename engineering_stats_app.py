
"""Engineering Statistics Interactive App (Streamlit)
Features:
- Upload CSV or use provided sample data
- Select a numeric column to analyze
- Shows: histogram, boxplot, time-series (if index/time col provided), summary stats (mean, std, CV, min, max)
- Detects outliers via 1.5*IQR and flags them in the table
- Simple "Gumbel quick estimate" for annual maxima (if the selected data are annual maxima)
- Export cleaned data (with outlier flag) as CSV
Requirements: streamlit, pandas, numpy, matplotlib, scipy
Run: pip install streamlit pandas numpy matplotlib scipy
     streamlit run engineering_stats_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO, BytesIO
from scipy import stats

st.set_page_config(page_title="Engineering Statistics Demo", layout="wide")

st.title("工程統計互動示範（Streamlit）")
st.markdown("""
這個互動 App 示範第1~2 章常用的資料檢視與基礎分析功能：
- 資料上傳或使用範例資料（20 年年最大日雨量）
- 選擇數值欄位進行分析（直方圖、箱型圖、時間序列）
- 自動計算平均、樣本標準差、CV、異常值標註
- 簡單 Gumbel 極值快速估計（供教學示範）
- 匯出帶有 outlier 標記的 CSV
""")

# Sidebar: data input
st.sidebar.header("Data input")
use_sample = st.sidebar.checkbox("Use sample dataset (20-year max daily rainfall)", value=True)

uploaded_file = None
if not use_sample:
    uploaded_file = st.sidebar.file_uploader("Upload CSV (first row header)", type=["csv"])

st.sidebar.markdown("---")
st.sidebar.write("If you upload a CSV, make sure it contains at least one numeric column.")

# Prepare data
sample_csv = """year,max_daily_rain_mm
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
    df = pd.read_csv(StringIO(sample_csv))
else:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.info("請上傳 CSV 或勾選左側的 sample dataset。")
        st.stop()

st.write("### 原始資料 (前 10 列)")
st.dataframe(df.head(10))

# Select numeric column
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if not numeric_cols:
    st.error("找不到數值欄位，請上傳包含數值欄位的 CSV。")
    st.stop()

col = st.selectbox("選擇要分析的數值欄位", numeric_cols)

data = df[col].dropna().astype(float).reset_index(drop=True)

st.write(f"選擇欄位 **{col}**，樣本數 n = {len(data)}")

# Compute stats
mean = data.mean()
std_s = data.std(ddof=1)  # sample std
cv = std_s / mean if mean != 0 else np.nan
mini = data.min()
maxi = data.max()

st.write("### 基本統計量")
st.metric("平均 (mean)", f"{mean:.3f}")
st.metric("樣本標準差 (s)", f"{std_s:.3f}")
st.metric("變異係數 (CV)", f"{cv:.3f}")
st.metric("最小 / 最大", f"{mini:.3f} / {maxi:.3f}")

# Outlier detection (1.5*IQR)
q1 = data.quantile(0.25)
q3 = data.quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
outlier_mask = (data < lower_bound) | (data > upper_bound)

st.write(f"IQR = {iqr:.3f}; Lower = {lower_bound:.3f}; Upper = {upper_bound:.3f}")
st.write(f"偵測到 {outlier_mask.sum()} 個異常值 (1.5*IQR 規則)")

# Plotting
fig, axes = plt.subplots(1,3, figsize=(15,4))
axes[0].hist(data, bins=8)
axes[0].set_title("Histogram")
axes[0].set_xlabel(col)
axes[0].set_ylabel("Frequency")

axes[1].boxplot(data, vert=False)
axes[1].set_title("Boxplot")

# If 'year' exists, plot time series
time_col = None
if 'year' in df.columns:
    time_col = 'year'
if time_col is None:
    # fallback to index
    axes[2].plot(data.values, marker='o', linestyle='-')
    axes[2].set_title("Index Series")
    axes[2].set_xlabel("Index")
else:
    axes[2].plot(df[time_col], data.values, marker='o', linestyle='-')
    axes[2].set_title("Time Series")
    axes[2].set_xlabel(time_col)

plt.tight_layout()
st.pyplot(fig)

# Show data with outlier flag
out_df = df.copy()
out_df['_analysis_value_'] = out_df[col].astype(float)
out_df['is_outlier_1.5IQR'] = outlier_mask.values
st.write("### Data with outlier flag (1.5*IQR)")
display_cols = [c for c in out_df.columns if c in ([time_col, col] if time_col else [col])]
display_cols += ['is_outlier_1.5IQR']
st.dataframe(out_df[display_cols].head(50))

# Gumbel quick-estimate (if data are annual maxima)
st.header("Gumbel Quick Estimate（教學示範）")
st.write("若所選資料為「年最大值」，可以用簡單方法估計 Gumbel 參數與超越機率（示範用）")
if len(data) < 5:
    st.info("樣本數太少，Gumbel 估計不可靠（需要更多年份）。")
else:
    beta = std_s / (np.pi / np.sqrt(6))
    gamma = 0.5772156649
    mu = mean - gamma * beta
    st.write(f"估計 β (scale) = {beta:.3f}, μ (location) = {mu:.3f}")
    x_val = st.number_input("計算 P(X ≥ x) 的 x 值（mm）", value=float(maxi))
    z = (x_val - mu) / beta
    Fx = np.exp(-np.exp(-z))
    p_exceed = 1 - Fx
    st.write(f"P(X ≥ {x_val:.1f}) ≈ {p_exceed*100:.3f} % (每年)")
    years = st.slider("累積年數（計算至少一次發生機率）", 1, 50, 10)
    p_10 = 1 - (1 - p_exceed) ** years
    st.write(f"{years} 年內至少一次發生的機率 ≈ {p_10*100:.3f} %")


# Allow export CSV with outlier flag
to_download = out_df.to_csv(index=False).encode('utf-8')
st.download_button("下載帶 outlier 標記的 CSV", data=to_download, file_name="data_with_outlier_flag.csv", mime="text/csv")

st.write("----")
st.write("教學提示：本 App 用途為教學示範。若要在工程設計中採用極值分析，請使用更嚴謹的參數估計（如 MLE 或 L-moments）並評估參數不確定性。")


