import streamlit as st
import random
import pandas as pd
st.title("自動出題與批改（教師工具）")
st.markdown("產生簡單的描述統計、小測題。學生作答後可即時批改。")

n = st.number_input("要出題數量", 1, 10, 3)
questions = []
answers = []

for i in range(int(n)):
    # generate random small dataset and ask mean/sd
    data = [round(random.uniform(0.2, 1.0),2) for _ in range(8)]
    q_text = f"資料: {data}，請計算平均與樣本標準差 (四捨五入到小數第二位)"
    mean = round(pd.Series(data).mean(),2)
    sd = round(pd.Series(data).std(ddof=1),2)
    questions.append(q_text)
    answers.append((mean, sd))

st.write("### 題目")
user_answers = []
for i,q in enumerate(questions):
    st.write(f"Q{i+1}: {q}")
    a1 = st.text_input(f"Q{i+1} 平均 (mean)", key=f"m{i}")
    a2 = st.text_input(f"Q{i+1} 樣本標準差 (s)", key=f"s{i}")
    user_answers.append((a1,a2))

if st.button("自動批改"):
    results = []
    for i,(ua,ub) in enumerate(user_answers):
        try:
            ma = float(ua); sa = float(ub)
        except:
            results.append("輸入格式錯誤")
            continue
        correct_mean, correct_sd = answers[i]
        mean_ok = abs(ma - correct_mean) < 0.02
        sd_ok = abs(sa - correct_sd) < 0.03
        results.append(f"Q{i+1}: mean {'OK' if mean_ok else 'WRONG'} (正確={correct_mean}), s {'OK' if sd_ok else 'WRONG'} (正確={correct_sd})")
    st.write("### 批改結果")
    for r in results:
        st.write(r)
