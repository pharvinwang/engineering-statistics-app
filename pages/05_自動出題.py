import streamlit as st
import numpy as np
from random import randint

from theme import apply_theme
apply_theme()

st.title("📝 自動出題與批改系統")

st.markdown('<div class="material-card">', unsafe_allow_html=True)
st.subheader("📘 產生題目")

a = randint(10, 50)
b = randint(1, 10)

st.write(f"題目：計算樣本 {a}, {b}, 20, 30 的平均值")
answer = (a + b + 20 + 30) / 4

user = st.number_input("你的答案：")
if st.button("批改"):
    if abs(user - answer) < 1e-6:
        st.success("答對了！")
    else:
        st.error(f"答錯了，正確答案是 {answer}")
st.markdown('</div>', unsafe_allow_html=True)
