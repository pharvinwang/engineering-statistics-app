import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from theme import apply_theme

# 套用 Material UI 主題
apply_theme()

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
st.title("🎲 Monte Carlo 風險模擬：結構可靠度 — Material UI 版")
st.markdown("""
本頁示範如何利用 **Monte Carlo 模擬**計算結構失效機率。

✅ 工程用途：
- 混凝土梁、擋土牆、坡穩分析  
- 考慮載重與材料強度隨機性  
- 預估 **可靠度 / 失效機率 Pf**
""")

# ============================================
# 名詞解釋
# ============================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📘 專有名詞說明（中等長度）")
st.markdown("""
- **可靠度 (Reliability, R)**：結構在給定載重下不失效的概率。  
- **失效機率 (Pf)**：結構失效的概率，Pf = 1 - Reliability。  
- **Margin (S - R)**：抵抗力 S 減去載重 R，Margin > 0 表示安全。  
- **隨機變數**：S 與 R 皆為隨機變數，反映材料、載重及環境的不確定性。  
- **用途**：工程師可透過 Monte Carlo 模擬評估不同設計條件下的失效風險，進而調整安全係數或材料選擇。  
後續章節會深入介紹如何依分布型態計算 Pf 與可靠度指標。
""")
st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# 使用者輸入
# ============================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("1️⃣ 輸入 S 與 R 的分布參數（假設常態）")

s_mu = st.number_input("S mean (µ_S)", value=120.0)
s_sd = st.number_input("S std (σ_S)", value=10.0)
r_mu = st.number_input("R mean (µ_R)", value=100.0)
r_sd = st.number_input("R std (σ_R)", value=15.0)
nrun = st.number_input("模擬次數 N", 1000, 200000, 10000)

st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# Monte Carlo 模擬
# ============================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("2️⃣ Monte Carlo 模擬與結果")

S = np.random.normal(s_mu, s_sd, int(nrun))
R = np.random.normal(r_mu, r_sd, int(nrun))
failure = (R > S)
pf = failure.mean()

st.write(f"➡ 估計失效機率 Pf ≈ {pf:.6f} ({pf*100:.4f}%)")
st.markdown("""
💡 說明：
- Monte Carlo 模擬是透過隨機生成大量樣本，估計結構在隨機載重下的失效比例。  
- Margin < 0 表示 R > S，結構失效。  
- 此方法適用於任意分布，不必限制於常態。
""")
st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# 繪圖區
# ============================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("3️⃣ 結果視覺化")

margin = S - R
fig, ax = plt.subplots(1, 2, figsize=(12, 4))

# Margin histogram
ax[0].hist(margin, bins=50)
ax[0].axvline(0, color='r', linestyle='--')
ax[0].set_title("Margin (S - R)")

# S & R overlay histogram
ax[1].hist(S, bins=30, alpha=0.6, label='S (抵抗力)')
ax[1].hist(R, bins=30, alpha=0.6, label='R (載重)')
ax[1].legend()
ax[1].set_title("S 與 R 分布")
st.pyplot(fig)

st.markdown("""
📌 觀察：
- 左圖 Margin < 0 的部分即為失效樣本  
- 右圖可比對載重與抵抗力分布，直覺理解結構安全性
""")
st.markdown("</div>", unsafe_allow_html=True)
