from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, DistilBertForSequenceClassification
import torch
import torch.nn.functional as F
import requests
import os
import re
import json

app = FastAPI()

# Путь к DistilBERT
DISTILBERT_PATH = os.getenv("DISTILBERT_PATH", "./models")

# Адрес llama-server (поднимается отдельным контейнером)
LLAMA_SERVER = os.getenv("LLAMA_SERVER", "http://llama:8080")

# DistilBERT
try:
    tokenizer = AutoTokenizer.from_pretrained(DISTILBERT_PATH)
    pt_model = DistilBertForSequenceClassification.from_pretrained(DISTILBERT_PATH)
except Exception as e:
    tokenizer, pt_model = None, None
    print(f"⚠️ Ошибка загрузки DistilBERT: {e}")


class EmailRequest(BaseModel):
    '''
    Класс для модели EmailRequest:

    text — текст письма для классификации
    model — строка, указывающая, какую модель использовать ("distilbert" или "mistral")
    '''
    text: str
    model: str = "distilbert" # по умолчанию


def run_distilbert(text: str):
    '''
    Функция для запуска модели DistilBERT:

    1. Проверяем наличие модели
    2. Токенизируем входной текст
    3. Передаем токены в модель
    
    Возвращаем JSON с меткой класса, вероятностью, причиной
    '''
    if tokenizer is None or pt_model is None:
        return {"label": "invalid", "reason": "Модель DistilBERT не загружена"}

    inputs = tokenizer(text, return_tensors="pt")
    outputs = pt_model(**inputs)
    probs = F.softmax(outputs.logits, dim=-1)

    label_id = torch.argmax(probs, dim=-1).item()
    score = probs[0][label_id].item()
    return {"label": "phishing" if label_id == 1 else "safe",
            "response_score": round(score, 2),
            "reason": "Классификация DistilBERT"}


# Mistral 7B Instruct
def run_mistral(text: str):
    '''
    Функция для запуска модели Mistral 7B Instruct через llama-server:

    1. Формируем промпт
    2. Отправляем POST-запрос на llama-server с промптом и параметрами генерации
    3. Ищем JSON в ответе модели
    
    Возвращаем JSON с меткой класса и причиной
    В случае ошибки возвращаем статус 'unknown' с объяснением
    '''
    prompt = f'''
    Ты — эксперт по кибербезопасности.
    Твоя задача — классифицировать письмо как 'Фишинг' или 'Нормальное'.
    Правила:
    - Возвращать только JSON.
    - Если нет ссылок, вложений или запросов персональных данных → "Нормальное".
    - Если есть подозрительные ссылки, вложения или запросы персональных данных → "Фишинг".

    Ответь строго в формате JSON:
    {{
      "label": "Фишинг" или "Нормальное",
      "reason": "Краткое объяснение без выдуманных фактов"
    }}

    Письмо: "{text}" 
    '''
    
    try:
        response = requests.post(f"{LLAMA_SERVER}/completion",
                                 json={"prompt": prompt, "n_predict": 64, "temperature": 0.7},
                                 timeout=90) # генерация занимает ~50 сек
        response.raise_for_status()
        raw = response.json().get("content", "").strip()

        if not raw:
            return {"label": "unknown", "reason": "Модель не вернула ответ"}

        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        else:
            return {"label": "Нормальное", "reason": "Не обнаружено признаков фишинга"}

    except Exception as e:
        return {"label": "unknown", "reason": f"Ошибка запроса к llama-server: {e}"}


# /predict
@app.post("/predict")
def predict_email(data: EmailRequest):
    '''
    Функция для обработки POST-запроса:

    1. Проверяем, что текст не пустой
    2. Проверяем, что в тексте есть латинские буквы (для DistilBERT)

    Вызываем функцию run_distilbert для 'distilbert' или run_mistral для 'mistral'
    В случае ошибки возвращаем сообщение об ошибке
    '''
    text = data.text.strip()
    if not text:
        return {"label": "invalid", "reason": "⚠️ Введите текст"}

    if data.model == "distilbert":
        if not re.search(r"[a-zA-Z]", text):
            return {"label": "invalid", "reason": "⚠️ Введите текст на английском языке"}
        return run_distilbert(text)

    elif data.model == "mistral":
        return run_mistral(text)

    else:
        return {"label": "invalid", "reason": "⚠️ Неизвестная модель"}
