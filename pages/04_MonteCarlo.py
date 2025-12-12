import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Monte Carlo 模擬", layout="wide")

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

# ===================================
# Title
# ===================================
st.title("🎲 Monte Carlo 風險模擬")

# ============================================================
# 📘 本章目標與工程用途
# ============================================================
st.markdown("""
<div class="material-title">📘 本章目標與工程用途</div>

Monte Carlo 模擬（MCS）是一種透過大量隨機抽樣，來估計工程事件風險的方法。  
在土木工程中非常常用，例如：

- 🌧️ **洪水風險評估**：計算未來 50 年出現大洪水的機率  
- 🏗️ **材料強度不確定性**：混凝土抗壓強度不足的機率  
- 🏞️ **邊坡穩定度 FOS < 1 的機率（滑動機率）**  
- 🚧 **結構荷重組合的超載風險**  

當數學公式難以推導時（例如參數太多、不確定性太強），MCS 是最直觀、最強大的方法。  
工程師常用它來回答：

- ❓「失敗機率是多少？」  
- ❓「多少年內會發生一次？」  
- ❓「如何量化不確定性？」  

本章將帶你用互動式介面，實際進行一次工程風險模擬。
""", unsafe_allow_html=True)

# ============================================================
# 📚 名詞定義與說明
# ============================================================
st.markdown("""
<div class="material-title">📚 名詞定義與說明</div>

### 🎯 **失效事件（Failure Event）**
在工程設計中，通常定義為：  
**當「負載 > 強度」時，系統失效**  
例如：
- 邊坡：外力 > 抗力  
- 結構：荷載 > 材料強度  
- 洪水：流量 > 堤防容量  

---

### 🎯 **隨機變數（Random Variables）**
在 MCS 中，所有不確定量都視為隨機變數，例如：
- 土壤黏聚力 ~ Normal(μ=25, σ=5)
- 風速 ~ Weibull(k, λ)
- 洪峰流量 ~ Lognormal

---

### 🎯 **失效機率（Probability of Failure, Pf）**
Pf = 失效次數 / 模擬總次數  
工程師最關心的就是這個值。

---

### 🎯 **可靠度指標 β（Reliability Index）**
Pf = Φ(-β)  
β 越大，代表越安全。

---

### 🎯 **Monte Carlo 的核心做法**
1. 從分布中產生大量樣本  
2. 每次模擬一次事件（是否失效）  
3. 統計失效比例 Pf  
4. 若需要，再推算 β  

---

這些概念後面章節會更深入，本章先讓你用直觀方式理解模擬過程。
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""<div class="material-title">🧪 互動式操作</div>""", unsafe_allow_html=True)

# ============================================================
# 🧪 Step 1：設定隨機分布
# ============================================================

st.subheader("Step 1：設定負載與強度的分布")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**📌 負載 Load（L）分布**")
    L_mean = st.number_input("負載平均值 μ_L", value=50.0)
    L_std = st.number_input("負載標準差 σ_L", value=10.0)

with col2:
    st.markdown("**📌 強度 Strength（R）分布**")
    R_mean = st.number_input("強度平均值 μ_R", value=80.0)
    R_std = st.number_input("強度標準差 σ_R", value=12.0)

# ============================================================
# 🧪 Step 2：模擬次數
# ============================================================

st.subheader("Step 2：設定模擬次數")
N = st.slider("模擬次數（越大越精準）", 1000, 1000000, 10000)

# ============================================================
# 🧪 Step 3：執行模擬
# ============================================================

st.subheader("Step 3：執行 Monte Carlo 模擬")

if st.button("▶ 開始模擬"):
    # 產生負載與強度樣本
    L_sample = np.random.normal(L_mean, L_std, N)
    R_sample = np.random.normal(R_mean, R_std, N)

    # 判斷失效
    failure = L_sample > R_sample
    Pf = failure.mean()

    # 可靠度 β
    from scipy.stats import norm
    beta = -norm.ppf(Pf) if Pf > 0 else np.inf

    st.success(f"失效機率 Pf = **{Pf:.4f}**")
    st.info(f"可靠度指標 β = **{beta:.3f}**")

    # Plot
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(L_sample, bins=40, alpha=0.6, label="Load L")
    ax.hist(R_sample, bins=40, alpha=0.6, label="Strength R")
    ax.set_title("負載與強度分布")
    ax.legend()
    st.pyplot(fig)

    # Download results
    result_df = pd.DataFrame({
        "Load_sample": L_sample,
        "Strength_sample": R_sample,
        "Failure": failure
    })
    csv = result_df.to_csv(index=False).encode("utf-8")
    st.download_button("下載模擬結果 CSV", csv, file_name="MonteCarlo_output.csv")

else:
    st.info("請按下『開始模擬』來執行 Monte Carlo")
