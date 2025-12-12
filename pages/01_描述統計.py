import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO
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
# 標題與 CSS
# ===================================
st.set_page_config(page_title="描述統計與資料探索", layout="wide")


st.title("📊 描述統計與資料探索")

# ===================================
# 本章目標與工程用途
# ===================================
st.markdown("""
<div class="material-card">
    <div class="material-title">📘 本章目標與工程用途</div>
    <div class="material-text">
        **本章主要目標：**
        - 了解工程資料的分布、平均值、變異及離散程度
        - 發現資料中的異常值，為工程決策提供依據

        **工程用途示例：**
        - 混凝土試體強度的品質管制
        - 土壤含水量一致性檢測
        - 降雨量統計與水土保持設計
    </div>
</div>
""", unsafe_allow_html=True)

# ===================================
# 名詞定義與說明
# ===================================
st.markdown("📚 **名詞定義與說明**")
st.markdown("""
- **平均值 (Mean)**：資料的集中趨勢
- **樣本標準差 (s)**：資料的離散程度
- **變異係數 (CV)**：標準差與平均值比率，用於比較不同量級的變異
- **IQR (Interquartile Range)**：上下四分位數距離，用於異常值偵測
- **異常值 (Outlier)**：明顯偏離其他觀測值的資料點

> 註：名詞定義中也說明工程用途，例如 CV 可用於比較不同材料或試樣之變異。
""")

st.markdown("---")
st.markdown("🧪 **互動式操作**")

# ===================================
# 上傳資料
# ===================================
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

# ===================================
# 數值欄位選擇與統計摘要
# ===================================
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

# ===================================
# 異常值偵測
# ===================================
q1 = data.quantile(0.25); q3 = data.quantile(0.75); iqr = q3 - q1
lower = q1 - 1.5*iqr; upper = q3 + 1.5*iqr
out_mask = (data < lower) | (data > upper)
st.write(f"IQR={iqr:.3f}, 下界={lower:.3f}, 上界={upper:.3f}，偵測到 {out_mask.sum()} 個異常值。")

# ===================================
# 視覺化
# ===================================
fig, axes = plt.subplots(1,3, figsize=(15,4))
axes[0].hist(data, bins=8)
axes[0].set_title("Histogram")
axes[1].boxplot(data, vert=False)
axes[1].set_title("Boxplot")
res = stats.probplot(data, dist="norm", plot=axes[2])
axes[2].set_title("QQ-plot")
st.pyplot(fig)

# ===================================
# 異常值列表與下載
# ===================================
st.write("### 異常值列表")
if out_mask.any():
    out_df = df.loc[out_mask.index[out_mask], df.columns]
    st.dataframe(out_df)
else:
    st.write("未偵測到異常值 (1.5*IQR)。")

df2 = df.copy()
df2['is_outlier_1.5IQR'] = out_mask.values
csv = df2.to_csv(index=False).encode('utf-8')
st.download_button("下載帶異常值標記的 CSV", csv, file_name="data_with_outlier_flag.csv", mime="text/csv")
