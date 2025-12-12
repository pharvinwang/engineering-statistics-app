import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import scipy.stats as stats
import matplotlib.pyplot as plt

# ============================================
# Material UI CSS
# ============================================
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
h1, h2, h3 {
    color: #1976d2;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# Title
# ============================================
st.title("📈 極值分析（Gumbel / GEV）— Material UI 版")

st.markdown("""
本頁示範工程常用的 **極值統計（Extreme Value Analysis）**：

- 適用於：  
  🌧 **最大日雨量**、最大風速、最大流量  
  🏗 **最大載重、材料強度極值**

- 本頁提供：  
  ✔ Gumbel 分布快速估計（工程常用）  
  ✔ 超越機率 P(X ≥ x)  
  ✔ N 年內至少一次發生的機率  
  ✔ 實測 CDF vs 模型 CDF 圖形  

---

### 📘 專有名詞快速解釋（讓學生更快上手）

#### **Gumbel 分布（Type I 極值）**
- 用途：描述「最大值」行為（降雨、風速、洪峰）  
- 工程意義：用來推估 **重現期 T-year rainfall** 或 **極端事件風險**

#### **GEV 分布（Generalized Extreme Value）**
- Gumbel 只是 GEV 的一種  
- 未來章節會說明 shape parameter ξ 如何決定尾端行為  

#### **重現期 Return Period (T-year)**
- T = 1 / 年 exceedance probability  
- 例如：  
  年超越機率 = 1% → 100 年重現期事件  

以上名詞在後面章節會完整推導，這裡先用「概念模式」讓同學建立工程上的感覺。
""")

# ============================================
# 資料上傳區
# ============================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("1️⃣ 資料上傳（每年一筆極值）")

uploaded = st.file_uploader("上傳 CSV（需含年度極值欄位）", type=["csv"])
use_sample = st.checkbox("使用範例資料 (20 年最大日雨量)", value=True)

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
        st.info("請上傳 CSV，或勾選使用範例資料。")
        st.stop()
    df = pd.read_csv(uploaded)

st.write("📄 **資料預覽**")
st.dataframe(df.head())
st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# 欄位選擇
# ============================================
numeric = df.select_dtypes(include=[np.number]).columns.tolist()
col = st.selectbox("選擇年最大值欄位", numeric)
data = df[col].dropna().astype(float)

# ============================================
# Gumbel 參數估計
# ============================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("2️⃣ Gumbel 參數快速估計（工程常用簡化法）")

mean = data.mean()
s = data.std(ddof=1)
beta = s / (np.pi / np.sqrt(6))
gamma = 0.5772156649
mu = mean - gamma * beta

st.write(f"樣本平均 = **{mean:.3f}**")
st.write(f"樣本標準差 = **{s:.3f}**")
st.success(f"Gumbel 估計參數： μ = **{mu:.3f}**,  β = **{beta:.3f}**")

st.markdown("""
📝 **說明**：  
這是工程常用的 Gumbel 參數取得方式，快速且在極值樣本不多時表現穩定。  
後續章節會介紹更精準的方法（MLE、L-moment）。
""")
st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# 超越機率
# ============================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("3️⃣ 計算超越機率 P(X ≥ x)")

x_val = st.number_input("輸入要評估的極值（例如 200 mm）", value=float(data.max()))

z = (x_val - mu) / beta
Fx = np.exp(-np.exp(-z))
p_exceed = 1 - Fx

st.write(f"➡ **年超越機率 P(X ≥ {x_val}) = {p_exceed*100:.4f}%**")

years = st.slider("累積年數", 1, 100, 10)
p_any = 1 - (1 - p_exceed)**years
st.success(f"📌 **{years} 年內至少一次發生機率： {p_any*100:.4f}%**")

st.markdown("""
📘 工程用途：  
- 設計雨水下水道  
- 判斷 50 年、100 年洪水量  
- 設施是否需強化或提高安全係數  
""")

st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# 圖形：Empirical vs Gumbel
# ============================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("4️⃣ 實測 CDF vs Gumbel CDF")

x = np.linspace(min(data)*0.8, max(data)*1.4, 200)
cdf_gumbel = np.exp(-np.exp(-(x - mu) / beta))

plt.figure(figsize=(8, 4))
plt.plot(np.sort(data),
         np.arange(1, len(data) + 1) / (len(data) + 1),
         marker='o', linestyle='none', label='Empirical')

plt.plot(x, cdf_gumbel, label='Gumbel CDF')
plt.xlabel(col)
plt.ylabel('Cumulative Probability')
plt.legend()

st.pyplot(plt)
st.markdown("</div>", unsafe_allow_html=True)
