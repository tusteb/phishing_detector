import pytest
import requests
import ui.predictor as predictor

# Фиктивный ответ API
class FakeResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"HTTP {self.status_code}")

def test_empty_text():
  '''
  Проверяем пустой ввод
  Ожидаем текст "Введите текст" и цвет "orange"
  '''
    result, color = predictor.predict("", model="distilbert")
    assert "Введите текст" in result
    assert color == "orange"

def test_invalid_model(monkeypatch):
  '''
  Проверяем неизвестную модель
  Ожидаем текст "Неизвестная модель" и цвет "orange"
  '''
    def fake_post(url, json, **kwargs):
        return FakeResponse({"label": "invalid", "reason": "⚠️ Неизвестная модель"})
    monkeypatch.setattr(predictor.requests, "post", fake_post)

    result, color = predictor.predict("Hello", model="unknown")
    assert "Неизвестная модель" in result
    assert color == "orange"

def test_distilbert_phishing(monkeypatch):
  '''
  Проверяем ответ модели distilbert на фишинговое письмо
  Ожидаем текст "Фишинговое письмо" и цвет "red"
  '''
    def fake_post(url, json, **kwargs):
        return FakeResponse({"label": "phishing", "response_score": 0.95})
    monkeypatch.setattr(predictor.requests, "post", fake_post)

    result, color = predictor.predict("Suspicious link", model="distilbert")
    assert "Фишинговое письмо" in result
    assert color == "red"

def test_distilbert_safe(monkeypatch):
  '''
  Проверяем ответ модели distilbert на безопасное письмо
  Ожидаем текст "Безопасное письмо" и цвет "green"
  '''
    def fake_post(url, json, **kwargs):
        return FakeResponse({"label": "safe", "response_score": 0.88})
    monkeypatch.setattr(predictor.requests, "post", fake_post)

    result, color = predictor.predict("Normal email", model="distilbert")
    assert "Безопасное письмо" in result
    assert color == "green"

def test_mistral_phishing(monkeypatch):
  '''
  Проверяем ответ модели mistral на фишинговое письмо
  Ожидаем текст "Фишинговое письмо" и цвет "red"
  '''
    def fake_post(url, json, **kwargs):
        return FakeResponse({"label": "Фишинг", "reason": "Подозрительная ссылка"})
    monkeypatch.setattr(predictor.requests, "post", fake_post)

    result, color = predictor.predict("Fake bank", model="mistral")
    assert "Фишинговое письмо" in result
    assert color == "red"

def test_mistral_normal(monkeypatch):
  '''
  Проверяем ответ модели mistral на безопасное письмо
  Ожидаем текст "Безопасное письмо" и цвет "green"
  '''
    def fake_post(url, json, **kwargs):
        return FakeResponse({"label": "Нормальное", "reason": "Обычное письмо"})
    monkeypatch.setattr(predictor.requests, "post", fake_post)

    result, color = predictor.predict("Привет!", model="mistral")
    assert "Безопасное письмо" in result
    assert color == "green"

def test_api_connection_error(monkeypatch):
  '''
  Проверяем ошибку соединения
  Ожидаем текст "Ошибка при подключении" и цвет "orange"
  '''
    def fake_post(url, json, **kwargs):
        raise requests.exceptions.ConnectionError("Connection failed")
    monkeypatch.setattr(predictor.requests, "post", fake_post)

    result, color = predictor.predict("Hello", model="distilbert")
    assert "Ошибка при подключении" in result
    assert color == "orange"
