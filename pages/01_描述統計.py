import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO
import scipy.stats as stats

# -----------------------------
# Material UI 友善樣式
# -----------------------------
st.markdown("""
<style>
/* 主要容器 */
.reportview-container .main .block-container {
    padding-top: 2rem;
}

/* 卡片樣式 */
.card {
    background: #ffffffaa;
    padding: 1.2rem 1.4rem;
    border-radius: 12px;
    border: 1px solid #e0e0e0;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 6px #00000015;
}

/* 標題配色 Material UI */
h1, h2, h3 {
    color: #1976d2;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------
st.title("📊 描述統計與視覺化（Material UI 版）")

st.markdown("""
本頁提供：

- 資料上傳或使用範例
- 統計摘要（mean, std, CV…）
- 直方圖、箱型圖、QQ-plot
- 1.5×IQR 異常值偵測  
""")

# -----------------------------
# 資料讀取卡片
# -----------------------------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📁 1. 載入資料")

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
            st.markdown("</div>", unsafe_allow_html=True)
            st.stop()
        df = pd.read_csv(uploaded)

    st.write("### 📄 資料預覽")
    st.dataframe(df.head())
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# 選擇欄位
# -----------------------------
numeric = df.select_dtypes(include=[np.number]).columns.tolist()
if not numeric:
    st.error("❌ 找不到任何數值欄位，請確認 CSV 格式。")
    st.stop()

with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔢 2. 選擇分析欄位")
    col = st.selectbox("選擇數值欄位", numeric)
    data = df[col].dropna().astype(float)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# 統計摘要 + CV
# -----------------------------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📈 3. 統計摘要（Summary Statistics）")

    st.write(data.describe().to_frame().T)

    mean = data.mean()
    s = data.std(ddof=1)
    cv = s / mean if mean != 0 else np.nan

    c1, c2, c3 = st.columns(3)
    c1.metric("平均值 Mean", f"{mean:.3f}")
    c2.metric("樣本標準差 s", f"{s:.3f}")
    c3.metric("變異係數 CV", f"{cv:.3f}")

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Outlier detection
# -----------------------------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🚨 4. 異常值偵測（1.5 × IQR）")

    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    out_mask = (data < lower) | (data > upper)

    st.write(f"IQR = **{iqr:.3f}**，範圍 = [{lower:.2f}, {upper:.2f}]")
    st.write(f"偵測到 **{out_mask.sum()}** 個異常值")

    if out_mask.any():
        st.dataframe(df.loc[out_mask.index[out_mask]])
    else:
        st.info("沒有偵測到異常值。")

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# 圖表
# -----------------------------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 5. 圖形分析")

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    axes[0].hist(data, bins=8)
    axes[0].set_title("Histogram")

    axes[1].boxplot(data, vert=False)
    axes[1].set_title("Boxplot")

    stats.probplot(data, dist="norm", plot=axes[2])
    axes[2].set_title("QQ-plot")

    st.pyplot(fig)

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Download result
# -----------------------------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⬇ 6. 下載結果")

    df2 = df.copy()
    df2["is_outlier_1.5IQR"] = out_mask.values
    csv = df2.to_csv(index=F_
