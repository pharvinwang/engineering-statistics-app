import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from theme import apply_theme

# 套用 Material UI 主題
apply_theme()

st.set_page_config(page_title="機率分布互動", page_icon="📈", layout="wide")

# ===============================
# 名詞定義卡片（Material UI）
# ===============================
st.markdown("""
<div class="material-card">
  <div class="material-title">📘 重要機率分布名詞定義與工程用途</div>
  <div class="material-text">

  <b>PDF：機率密度函數（Probability Density Function）</b><br>
  描述變數「在哪些數值附近較常出現」。  
  工程用途：材料強度分布、降雨強度分布、風速分布、交通流量分布等。  
  <br><br>

  <b>CDF：累積機率函數（Cumulative Distribution Function）</b><br>
  描述某數值以下的累積機率，例如「雨量小於 100 mm 的機率」。  
  <br>
  工程用途：判斷安全界限、計算達標率、評估合格率、風險之下限估計。  
  <br><br>

  <b>超越機率 Exceedance Probability</b><br>
  指「某事件超過指定門檻的機率」。  
  工程用途：  
  - 降雨大於 200 mm 的機率  
  - 混凝土強度低於設計值的機率  
  - 風速超過設計基準的機率  
  <br><br>

  <b>百分位數 Percentile</b><br>
  「資料中，有多少比例會低於某個值」。  
  工程用途：  
  - 設計暴雨量（如 95 百分位）  
  - 材料最小保證強度（如 5 百分位）  
  <br><br>

  <b>三個常用工程分布：</b><br>
  <b>正態分布 Normal：</b> 用於誤差、材料尺寸、測量誤差。  
  <br>
  <b>對數正態 Lognormal：</b> 用於非負資料，如降雨、流量、材料強度。  
  <br>
  <b>威布爾 Weibull：</b> 用於風速、材料破壞機率、壽命分布。  
  <br><br>

  （註：後續「工程極值分析」將補充 GEV 分布處理最大事件。）
  </div>
</div>
""", unsafe_allow_html=True)

# ===============================
# 分布選單
# ===============================
st.title("📈 機率分布互動模組")

dist_name = st.selectbox(
    "選擇分布類型",
    ["Normal（正態）", "Lognormal（對數正態）", "Weibull（威布爾）"]
)

# ===============================
# 參數輸入
# ===============================
st.subheader("🧮 分布參數設定")

if dist_name == "Normal（正態）":
    mu = st.number_input("平均值 μ", value=50.0)
    sigma = st.number_input("標準差 σ", value=10.0, min_value=0.001)
    dist = stats.norm(mu, sigma)
    param_text = f"μ = {mu}, σ = {sigma}"

elif dist_name == "Lognormal（對數正態）":
    mean = st.number_input("對數平均 μ_log", value=3.0)
    sd = st.number_input("對數標準差 σ_log", value=0.25, min_value=0.001)
    dist = stats.lognorm(s=sd, scale=np.exp(mean))
    param_text = f"μ_log = {mean}, σ_log = {sd}"

elif dist_name == "Weibull（威布爾）":
    shape = st.number_input("形狀參數 k", value=2.0, min_value=0.1)
    scale = st.number_input("尺度參數 λ", value=50.0, min_value=0.1)
    dist = stats.weibull_min(shape, scale=scale)
    param_text = f"k = {shape}, λ = {scale}"

# ===============================
# 顯示參數
# ===============================
st.info(f"📌 分布參數：{param_text}")

# ===============================
# 繪圖：PDF & CDF
# ===============================
st.subheader("📊 PDF / CDF 圖形")

x = np.linspace(dist.ppf(0.001), dist.ppf(0.999), 200)

fig, ax = plt.subplots(1, 2, figsize=(14, 4))

ax[0].plot(x, dist.pdf(x))
ax[0].set_title("PDF（機率密度函數）")
ax[0].set_xlabel("x")
ax[0].set_ylabel("density")

ax[1].plot(x, dist.cdf(x))
ax[1].set_title("CDF（累積機率函數）")
ax[1].set_xlabel("x")
ax[1].set_ylabel("probability")

st.pyplot(fig)

# ===============================
# 超越機率查詢
# ===============================
st.subheader("🎯 超越機率查詢 (P(X > x))")

threshold = st.number_input("輸入門檻 x", value=60.0)

p_exceed = 1 - dist.cdf(threshold)
st.metric("超越機率", f"{p_exceed:.4f}")

# ===============================
# 百分位數查詢
# ===============================
st.subheader("📌 百分位數查詢（Percentile）")

pctl = st.slider("選擇百分位數 (%)", 1, 99, 95)
value_pctl = dist.ppf(pctl / 100)
st.metric(f"{pctl} 百分位值", f"{value_pctl:.3f}")

# ===============================
# 額外工程應用說明區（Material UI）
# ===============================
st.markdown(f"""
<div class="material-card">
  <div class="material-title">🔍 工程應用說明：{dist_name}</div>
  <div class="material-text">

  <b>Normal（正態）用途：</b><br>
  • 混凝土抗壓強度（高品質材料）  
  • 施工誤差、量測誤差  
  • 材料尺寸公差  
  <br><br>

  <b>Lognormal（對數正態）用途：</b><br>
  • 雨量、流量（皆為非負且右偏）  
  • 土壤滲透係數  
  • 破壞強度資料常呈對數正態分布  
  <br><br>

  <b>Weibull（威布爾）用途：</b><br>
  • 風速分布（氣象工程最常見）  
  • 材料疲勞壽命、破壞機率  
  • 可靠度工程（壽命模型）  
  <br><br>

  （註：後續「極值與 GEV」頁面將介紹最大值事件，不同於本頁面的常態資料分析。）
  </div>
</div>
""", unsafe_allow_html=True)
