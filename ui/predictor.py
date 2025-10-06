import re
import requests
from .preprocess import clean_text

API_URL = "http://api:8000/predict"

def predict(text: str):
    if not text.strip() or not re.search(r"[a-zA-Z]", text):
        return "⚠️ Введите текст на английском языке", "orange"

    try:
        response = requests.post(API_URL, json={"text": text})
        data = response.json()

        if data["label"] == "phishing":
            return f"🟠 Фишинговое письмо<br>(уверенность {data['response_score']:.2f})", "red"
        elif data["label"] == "safe":
            return f"🟢 Безопасное письмо<br>(уверенность {data['response_score']:.2f})", "green"
        else:
            return data["result"], "orange"
    except Exception as e:
        return f"❌ Ошибка при подключении к API: {e}", "orange"
