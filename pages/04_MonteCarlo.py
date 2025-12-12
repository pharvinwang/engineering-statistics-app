import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ============================================
# Material UI 套用
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
    margin-bottom: 0.5rem;
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
    margin-right: 5px;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# Page Title
# ============================================
st.title("🎲 Monte Carlo 工程可靠度模擬")

# ============================================
# 工程用途卡片
# ============================================
st.markdown("""
<div class="material-card">
    <div class="material-title">📘 為什麼需要 Monte Carlo？（工程用途）</div>
    <div class="material-text">
Monte Carlo 模擬是工程界最常用的風險分析工具之一，用來估計「不確定性」帶來的安全風險。  
常見應用包含：

- 邊坡穩定（強度 / 受力變異 → 崩塌機率）
- 洪峰流量推估（降雨變化 → 超標機率）
- 結構承載力（材料強度變異 → 破壞機率）
- 混凝土/鋼筋設計（荷載 vs. 強度 → 安全度評估）

其核心計算公式為：

<div class="material-badge">失效機率 Pf = P(g(X) &lt; 0)</div>
<div class="material-badge">可靠度 β = -Φ⁻¹(Pf)</div>

其中  
**g(X)** 為 Limit State（極限狀態）  
**Pf** 為失敗的機率  
**β（Beta Index）** 為可靠度指標，多用於結構工程的安全設計。
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# 名詞定義卡片
# ============================================
st.markdown("""
<div class="material-card">
    <div class="material-title">📚 名詞定義（基礎版）</div>
    <div class="material-text">
**📌 Limit State Function（極限狀態式）**  
用來判斷結構是否安全：  
g(X) = Resistance – Load  
g(X) &lt; 0 → 失效  

**📌 Pf（Failure Probability，失效機率）**  
系統在隨機條件下發生失敗的機率。

**📌 β（Reliability Index，可靠度指標）**  
反映結構的安全程度，β 越高越安全。  
土木結構常見 β = 3.0 ~ 4.0。

**📌 Monte Carlo Simulation**  
大量隨機生成樣本（通常 1,000 ~ 1,000,000 次），  
用於模擬實際工程中的不確定性與變動。
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# Input Section
# ============================================
st.header("🧮 Step 1. 定義隨機變數（Load vs Strength）")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 強度 (Resistance)")
    R_mean = st.number_input("平均 Strength μ_R", value=100.0)
    R_std = st.number_input("標準差 σ_R", value=10.0)

with col2:
    st.subheader("📌 荷載 (Load)")
    L_mean = st.number_input("平均 Load μ_L", value=80.0)
    L_std = st.number_input("標準差 σ_L", value=8.0)

st.header("🎛 Step 2. 模擬設定")

N = st.number_input("Monte Carlo 模擬次數 N", value=5000, step=1000)

# ============================================
# Simulation
# ============================================
if st.button("開始模擬 🎲"):
    R = np.random.normal(R_mean, R_std, N)
    L = np.random.normal(L_mean, L_std, N)
    g = R - L  # Limit state
    
    Pf = np.mean(g < 0)
    
    if Pf > 0:
        beta = -stats.norm.ppf(Pf)
    else:
        beta = np.inf

    st.success(f"📌 **失效機率 Pf = {Pf:.6f}**")
    st.info(f"📌 **可靠度指標 β = {beta:.3f}**")

    # Plot
    plt.figure(figsize=(8,4))
    plt.hist(g, bins=30)
    plt.axvline(0, linestyle="--")
    plt.title("Distribution of g(X) = R - L")
    plt.xlabel("g")
    st.pyplot(plt)

    st.write("下表為部分模擬結果（前 20 筆）")
    st.dataframe(
        {"R": R[:20], "L": L[:20], "g": g[:20]}
    )
