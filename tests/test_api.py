import pytest
from fastapi.testclient import TestClient
import api.api

client = TestClient(api.api.app)

def test_empty_text(monkeypatch):
    '''
    Функция для проверки ввода пустого текста в модель distilbert
    Ожидаем label "invalid" и сообщение "Введите текст"
    '''
    def fake_run_distilbert(text):
        return {"label": "invalid", "reason": "Введите текст"}
    monkeypatch.setattr(api.api, "run_distilbert", fake_run_distilbert)

    response = client.post("/predict", json={"text": "", "model": "distilbert"})
    data = response.json()
    assert data["label"] == "invalid"
    assert "Введите текст" in data["reason"]

def test_invalid_model():
    '''
    Функция для проверки неизвестной модели
    Ожидаем label "invalid" и сообщение "Неизвестная модель"
    '''
    response = client.post("/predict", json={"text": "Hello world", "model": "unknown"})
    data = response.json()
    assert data["label"] == "invalid"
    assert "Неизвестная модель" in data["reason"]

def test_distilbert_non_english(monkeypatch):
    '''
    Функция для проверки ввода текста не на английском языке в модель distilbert
    Ожидаем label "invalid" и сообщение "Введите текст на английском языке"
    '''
    def fake_run_distilbert(text):
        return {"label": "invalid", "reason": "Введите текст на английском языке"}
    monkeypatch.setattr(api.api, "run_distilbert", fake_run_distilbert)

    response = client.post("/predict", json={"text": "Привет мир", "model": "distilbert"})
    data = response.json()
    assert data["label"] == "invalid"
    assert "Введите текст на английском языке" in data["reason"]

# Входные данные
@pytest.mark.parametrize("text,label", [("Suspicious link http://phishing.com", "phishing"),
                                        ("Normal safe email with no links", "safe")])

def test_distilbert_classification(monkeypatch, text, label):
    '''
    Функция для проверки классификации distilbert
    Ожидаем label и response_score (float)
    '''
    def fake_run_distilbert(t):
        return {"label": label, "response_score": 0.9, "reason": "Тест"}
    monkeypatch.setattr(api.api, "run_distilbert", fake_run_distilbert)

    response = client.post("/predict", json={"text": text, "model": "distilbert"})
    data = response.json()
    assert data["label"] == label
    assert isinstance(data["response_score"], float)

def test_mistral_classification(monkeypatch):
    '''
    Функция для проверки генерации mistral
    Ожидаем label и reason ("Тестовый ответ")
    '''
    def fake_run_mistral(text):
        return {"label": "Нормальное", "reason": "Тестовый ответ"}
    monkeypatch.setattr(api.api, "run_mistral", fake_run_mistral)

    response = client.post("/predict", json={"text": "Привет!", "model": "mistral"})
    data = response.json()
    assert data["label"] == "Нормальное"
    assert "Тестовый ответ" in data["reason"]
