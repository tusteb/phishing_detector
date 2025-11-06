from fastapi import FastAPI, Request
from pydantic import BaseModel
from preprocess import clean_text
from transformers import AutoTokenizer, TFDistilBertForSequenceClassification, pipeline
import re

app = FastAPI()

# Загрузка модели и токенизатора
tokenizer = AutoTokenizer.from_pretrained("model")
model = TFDistilBertForSequenceClassification.from_pretrained("model")
nlp = pipeline("text-classification", model=model, tokenizer=tokenizer, framework="tf")

class EmailRequest(BaseModel):
    '''
    Класс для описания входных данных
    '''
    text: str

# Эндпоинт /predict
@app.post("/predict")
def predict_email(data: EmailRequest):
    '''
    Функция для получения предсказания модели на основе вводимого текста:

    1. Принимаем текст письма
    2. Проверяем, что текст не пустой и содержит латинские буквы
    3. Предобрабатываем текст через функцию clean_text
    4. Если после очистки текст пустой - возвращаем ошибку 'invalid'
    
    Возвращаем результат, метку класса и вероятность
    '''
    text = data.text
    if not text.strip() or not re.search(r"[a-zA-Z]", text):
        return {"result": "⚠️ Введите тект на английском языке", "label": "invalid"}

    cleaned = clean_text(text)
    if not cleaned:
        return {"result": "⚠️ Введите тект на английском языке", "label": "invalid"}

    result = nlp(cleaned)[0]
    label = result["label"]
    score = result["score"]

    if label == 'LABEL_1':
        return {"result": "🟠 Фишинговое письмо",
                "response_score": round(score, 2),
                "label": "phishing"}
    else:
        return {"result": "🟢 Безопасное письмо",
                "response_score": round(score, 2),
                "label": "safe"}
