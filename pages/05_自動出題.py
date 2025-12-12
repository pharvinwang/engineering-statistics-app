import streamlit as st
import random
import pandas as pd

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
.stTextInput>div>input {
    border-radius: 6px;
    border: 1px solid #b0b0b0;
    padding: 6px;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# Title & Intro
# ============================================
st.title("📝 自動出題與批改（教師工具）")
st.markdown("""
本頁可生成 **隨機小型描述統計題**，學生輸入答案後即時批改。  

📌 工程用途：
- 適合課堂練習或線上測驗
- 提升學生對平均值與標準差的敏感度
- 後續章節會有更複雜統計題型
""")

# ============================================
# 產生題目數量
# ============================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
n = st.number_input("要出題數量", 1, 10, 3)
st.markdown("</div>", unsafe_allow_html=True)

questions = []
answers = []

# 產生題目
for i in range(int(n)):
    data = [round(random.uniform(0.2, 1.0), 2) for _ in range(8)]
    q_text = f"資料: {data}，請計算平均與樣本標準差 (四捨五入到小數第二位)"
    mean = round(pd.Series(data).mean(), 2)
    sd = round(pd.Series(data).std(ddof=1), 2)
    questions.append(q_text)
    answers.append((mean, sd))

# ============================================
# 顯示題目與輸入欄
# ============================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("1️⃣ 題目區 & 學生作答")

user_answers = []
for i, q in enumerate(questions):
    st.markdown(f"**Q{i+1}:** {q}")
    a1 = st.text_input(f"Q{i+1} 平均 (mean)", key=f"m{i}")
    a2 = st.text_input(f"Q{i+1} 樣本標準差 (s)", key=f"s{i}")
    user_answers.append((a1, a2))

st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# 自動批改
# ============================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("2️⃣ 批改結果")

if st.button("自動批改"):
    results = []
    for i, (ua, ub) in enumerate(user_answers):
        try:
            ma = float(ua)
            sa = float(ub)
        except:
            results.append(f"Q{i+1}: 輸入格式錯誤")
            continue
        correct_mean, correct_sd = answers[i]
        mean_ok = abs(ma - correct_mean) < 0.02
        sd_ok = abs(sa - correct_sd) < 0.03
        results.append(
            f"Q{i+1}: mean {'✅' if mean_ok else '❌'} (正確={correct_mean}), "
            f"s {'✅' if sd_ok else '❌'} (正確={correct_sd})"
        )

    # 顯示結果
    for r in results:
        st.write(r)
st.markdown("</div>", unsafe_allow_html=True)
