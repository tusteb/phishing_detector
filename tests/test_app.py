import pytest
from ui.predictor import predict

def test_empty_input():
    msg, color = predict("")
    assert "Введите текст" in msg
    assert color == "orange"

def test_non_english_input():
    msg, color = predict("Привет, это письмо")
    assert "Введите текст" in msg
    assert color == "orange"

def test_api_error(monkeypatch):
    def fake_post(*args, **kwargs):
        raise Exception("API недоступно")
    import ui.predictor as predictor
    monkeypatch.setattr(predictor.requests, "post", fake_post)

    msg, color = predictor.predict("Hello, world")
    assert "Ошибка при подключении" in msg
    assert color == "orange"
