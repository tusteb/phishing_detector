import os
import requests
from ui.preprocess import clean_text

# Адрес API
API_URL = os.getenv("API_URL", "http://api:8000/predict")

def predict(text: str, model: str = "distilbert"): 
    '''
    Функция для получения предсказания:

    1. Проверяем, если текст пустой
    2. Предобрабатывем текст для DistilBERT
    3. Отправляем запрос к API (с тайм-аутом 90 сек для Mistral)
    4. Обрабатываем ошибки сети (RequestException)

    Возвращаем ответ модели и цвет ответа для UI
    '''
    if not text.strip():
        return "⚠️ Введите текст", "orange"

    # Очистка текста только для DistilBERT
    if model == "distilbert":
        text = clean_text(text)

    try:
        response = requests.post(API_URL, json={"text": text, "model": model}, timeout=90)
        response.raise_for_status()
        data = response.json()

        # DistilBERT
        if model == "distilbert":
            label = data.get("label", "invalid")
            score = data.get("response_score", 0.0)
            if label == "phishing":
                return f"🟠 Фишинговое письмо<br>(уверенность {score:.2f})", "red"
            elif label == "safe":
                return f"🟢 Безопасное письмо<br>(уверенность {score:.2f})", "green"
            else:
                return data.get("reason", "⚠️ Неизвестный ответ"), "orange"

        # Mistral (через llama-server)
        elif model == "mistral":
            label = data.get("label", "unknown").lower()
            reason = data.get("reason", "")
            if label in ["фишинг", "phishing"]:
                return f"🔴 Фишинговое письмо<br>{reason}", "red"
            elif label in ["нормальное", "safe"]:
                return f"🟢 Безопасное письмо<br>{reason}", "green"
            else:
                return reason or "⚠️ Неизвестный ответ", "orange"

        # Неизвестная модель
        else:
            return "⚠️ Неизвестная модель", "orange"

    except requests.exceptions.RequestException as e:
        return f"❌ Ошибка при подключении к API: {e}", "orange"
