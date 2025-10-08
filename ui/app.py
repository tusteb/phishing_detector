import streamlit as st
import time
from predictor import predict

st.set_page_config(page_title="Phishing Detector")
st.markdown("# 📧 Phishing-detector")
st.markdown("Введите текст e-mail, чтобы получить предсказание модели и уровень её уверенности.")
st.markdown("⚠️ Модель обучена на англоязычных письмах, поэтому вводите текст на **английском языке**.")

text_input = st.text_area("Текст письма на английском языке", height=250)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("**Проверить**", use_container_width=True):
        with st.spinner("Анализируем e-mail..."):
            time.sleep(0.5)
            message, color = predict(text_input)
        st.markdown(f"""
                    <div style='text-align: center; color:{color}; font-weight:bold; font-size:18px;'>
                        {message}
                    </div>
                    """, unsafe_allow_html=True)
