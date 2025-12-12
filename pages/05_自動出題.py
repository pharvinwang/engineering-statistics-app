import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="自動出題系統", layout="wide")
st.title("📝 自動出題系統")

# ============================================================
# 📘 本章目標與工程用途
# ============================================================
st.markdown("""
<div class="material-title">📘 本章目標與工程用途</div>

本章提供一個能 **自動產生工程統計題目** 的互動平台，讓學生可以：

- 反覆練習「平均、標準差、CV、機率、極值」等工程統計核心技能  
- 練習單位轉換與工程判讀  
- 自動批改答案，立即回饋  
- 提供多樣題目類型，支援隨機數據  

工程應用包括：  
- 混凝土抗壓強度的變異分析  
- 土壤含水量、單位重、C / φ 不確定性  
- 降雨極值與重現期  
- 結構荷重組合的機率問題  

適合用於課堂練習、課後作業、自主學習。
""", unsafe_allow_html=True)

# ============================================================
# 📚 名詞定義與說明
# ============================================================
st.markdown("""
<div class="material-title">📚 名詞定義與說明</div>

### 📌 平均值（Mean）
工程中常用於表示材料或環境參數的「典型值」。

### 📌 標準差（Standard Deviation）
衡量資料的離散程度；變異越大 → 不確定性越高。

### 📌 變異係數 CV = s / μ
衡量資料相對變異性，工程材料常以 CV 作為品質穩定度指標。

### 📌 超越機率（Exceedance Probability）
工程風險評估的重要量，例如：  
雨量 > 200 mm 的機率、風速 > 50 m/s 的機率等。

以上概念皆為後續工程設計、可靠度分析的基礎。
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""<div class="material-title">🧪 互動式操作</div>""", unsafe_allow_html=True)

# ============================================================
# 🧪 題目選擇
# ============================================================
st.subheader("Step 1：選擇題目類型")

question_type = st.selectbox(
    "請選擇題型",
    [
        "1️⃣ 平均與標準差",
        "2️⃣ 變異係數（CV）",
        "3️⃣ 單一常態分布機率",
        "4️⃣ GEV 極值與重現期",
    ]
)

st.markdown("---")

# ============================================================
# 🧪 Step 2：自動出題
# ============================================================

st.subheader("Step 2：自動出題")

if st.button("🎲 生成題目"):
    if question_type == "1️⃣ 平均與標準差":
        data = np.random.randint(10, 100, size=6)
        st.session_state["question"] = f"資料為：{data.tolist()}，請計算平均與樣本標準差。"
        st.session_state["answer_mean"] = np.mean(data)
        st.session_state["answer_std"] = np.std(data, ddof=1)

    elif question_type == "2️⃣ 變異係數（CV）":
        mean = np.random.uniform(20, 100)
        sd = np.random.uniform(2, 20)
        st.session_state["question"] = f"某材料平均強度 μ = {mean:.2f}，標準差 σ = {sd:.2f}，求 CV。"
        st.session_state["answer_cv"] = sd / mean

    elif question_type == "3️⃣ 單一常態分布機率":
        mean = np.random.uniform(30, 80)
        sd = np.random.uniform(5, 20)
        x = np.random.uniform(20, 100)
        from scipy.stats import norm
        prob = 1 - norm.cdf(x, mean, sd)

        st.session_state["question"] = (
            f"某材料強度 X ~ N({mean:.1f}, {sd:.1f})，求 P(X > {x:.1f})。"
        )
        st.session_state["answer_prob"] = prob

    elif question_type == "4️⃣ GEV 極值與重現期":
        mu = np.random.uniform(80, 150)
        sigma = np.random.uniform(5, 25)
        xi = np.random.uniform(-0.2, 0.2)
        x = np.random.uniform(100, 200)
        from scipy.stats import genextreme as gev

        prob = 1 - gev.cdf(x, -xi, mu, sigma)
        T = 1 / prob if prob > 0 else np.inf

        st.session_state["question"] = (
            f"GEV 參數：μ={mu:.1f}, σ={sigma:.1f}, ξ={xi:.2f}，求 x={x:.1f} 的重現期 T。"
        )
        st.session_state["answer_T"] = T

# 顯示題目
if "question" in st.session_state:
    st.markdown(f"### 📄 題目：{st.session_state['question']}")

st.markdown("---")

# ============================================================
# 🧪 Step 3：作答與批改
# ============================================================
st.subheader("Step 3：作答與即時批改")

if question_type == "1️⃣ 平均與標準差":
    ans_mean = st.number_input("你的平均值答案：", value=0.0)
    ans_std = st.number_input("你的標準差答案：", value=0.0)

    if st.button("📝 批改"):
        st.write(f"正確平均 = **{st.session_state['answer_mean']:.3f}**")
        st.write(f"正確標準差 = **{st.session_state['answer_std']:.3f}**")

        diff_mean = abs(ans_mean - st.session_state["answer_mean"])
        diff_std = abs(ans_std - st.session_state["answer_std"])

        if diff_mean < 0.5 and diff_std < 0.5:
            st.success("✔ 很棒！你的答案非常接近！")
        else:
            st.error("✘ 再試試看，你的答案誤差較大。")

elif question_type == "2️⃣ 變異係數（CV）":
    ans_cv = st.number_input("你的 CV 答案：", value=0.0)

    if st.button("📝 批改"):
        real = st.session_state["answer_cv"]
        st.write(f"正確 CV = **{real:.4f}**")
        diff = abs(ans_cv - real)

        if diff < 0.05:
            st.success("✔ 正確！")
        else:
            st.error("✘ 誤差較大，再試試！")

elif question_type == "3️⃣ 單一常態分布機率":
    ans_prob = st.number_input("你的 P(X>a) 答案：", value=0.0)

    if st.button("📝 批改"):
        real = st.session_state["answer_prob"]
        st.write(f"正確機率 = **{real:.4f}**")

        if abs(ans_prob - real) < 0.05:
            st.success("✔ 接近！")
        else:
            st.error("✘ 差距大，再算一次。")

elif question_type == "4️⃣ GEV 極值與重現期":
    ans_T = st.number_input("你的重現期 T：", value=1.0)

    if st.button("📝 批改"):
        real = st.session_state["answer_T"]
        st.write(f"正確 T = **{real:.1f} 年**")

        if abs(ans_T - real) / real < 0.2:
            st.success("✔ 還不錯！你的誤差在 20% 內。")
        else:
            st.error("✘ 誤差太大，再試一次！")

