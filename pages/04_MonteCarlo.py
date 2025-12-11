import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("Monte Carlo 風險模擬：簡易結構可靠度")
st.markdown("示範：結構受力 R 與抵抗 S，計算失效概率 P(S < R)")

# User inputs distributions for R and S (normal for demo)
st.subheader("輸入抵抗 S（strength）與載重 R（load）分布參數（假設常態）")
s_mu = st.number_input("S mean (µ_S)", value=120.0)
s_sd = st.number_input("S std (σ_S)", value=10.0)
r_mu = st.number_input("R mean (µ_R)", value=100.0)
r_sd = st.number_input("R std (σ_R)", value=15.0)
nrun = st.number_input("模擬次數 (N)", 1000, 200000, 10000)

# Monte Carlo
S = np.random.normal(s_mu, s_sd, int(nrun))
R = np.random.normal(r_mu, r_sd, int(nrun))
failure = (R > S)
pf = failure.mean()
st.write(f"估計失效機率 P_f ≈ {pf:.6f} ({pf*100:.4f}%)")

# Plot histogram of margin (S-R)
margin = S - R
fig, ax = plt.subplots(1,2, figsize=(12,4))
ax[0].hist(margin, bins=50)
ax[0].axvline(0, color='r', linestyle='--')
ax[0].set_title("Margin (S - R)")
ax[1].hist(S, bins=30, alpha=0.6, label='S')
ax[1].hist(R, bins=30, alpha=0.6, label='R')
ax[1].legend()
st.pyplot(fig)

st.write("說明：若 margin < 0 表示 R > S（失效）。Monte Carlo 可用在任何分布，只需改變隨機樣本生成方式。")
