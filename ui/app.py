import streamlit as st
import time
from ui.predictor import predict

# Настройки страницы
st.set_page_config(page_title="Phishing Detector")
st.markdown("# 📧 Phishing-detector")
st.markdown("Введите текст e-mail, чтобы получить предсказание модели и уровень её уверенности.")

# Переключатель модели
model_choice = st.radio("Выберите модель для анализа:",
                        ("DistilBERT", "Mistral 7B Instruct"),
                        horizontal=True,
                        index=0)

# Предупреждение только для DistilBERT
if model_choice == "DistilBERT":
    st.markdown("⚠️ Модель обучена на англоязычных письмах, поэтому вводите текст на **английском языке**.")

# Поле ввода текста
text_input = st.text_area("Текст письма", height=250)

# Кнопка запуска анализа
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("**Проверить**", use_container_width=True):
        if not text_input.strip():
            st.warning("⚠️ Введите текст для анализа")
        else:
            # Определяем выбранную модель
            if model_choice == "Mistral 7B Instruct":
                spinner_text = "Mistral думает..."
                model_name = "mistral"
            else:
                spinner_text = "DistilBERT думает..."
                model_name = "distilbert"

            with st.spinner(spinner_text):
                message, color = predict(text_input, model=model_name)

            st.markdown(f"""
                        <div style='text-align: center; color:{color}; font-weight:bold; font-size:18px;'>
                            {message}
                        </div>
                        """,
                        unsafe_allow_html=True)
