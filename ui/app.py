import streamlit as st
import re
import time
from preprocess import clean_text
import requests

API_URL = "http://api:8000/predict"

def query_api(text: str):
    if not text.strip() or not re.search(r"[a-zA-Z]", text):
        return "⚠️ Введите текст на английском языке", "orange"

    try:
        response = requests.post(API_URL, json={"text": text})
        data = response.json()

        if data["label"] == "phishing":
            message = f"🟠 Фишинговое письмо<br>(уверенность {data['response_score']:.2f})"
            color = "red"
        elif data["label"] == "safe":
            message = f"🟢 Безопасное письмо<br>(уверенность {data['response_score']:.2f})"
            color = "green"
        else:
            message = data["result"]
            color = "orange"

        return message, color

    except Exception as e:
        return f"❌ Ошибка при подключении к API: {e}", "orange"


st.set_page_config(page_title="Phishing Detector")
st.markdown("# 📧 Phishing-detector")
st.markdown("Введите текст e-mail, чтобы получить предсказание модели и уровень её уверенности.")
st.markdown("Обращаем внимание, что модель обучена на англоязычных письмах, поэтому вводите текст на **английском языке**, пожалуйста.")

text_input = st.text_area("Текст письма на английском языке", height=250)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("**Проверить**", use_container_width=True):
        with st.spinner("Анализируем e-mail..."):
            time.sleep(0.5)
            message, color = query_api(text_input)
        st.markdown(f"""
                        <div style='text-align: center; color:{color}; font-weight:bold; font-size:18px;'>
                            {message}
                        </div>
                    """, unsafe_allow_html=True)