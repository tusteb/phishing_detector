import pytest
import ui.predictor as predictor

@pytest.fixture(autouse=True)
def mock_model(monkeypatch):
    monkeypatch.setattr("transformers.AutoTokenizer.from_pretrained",
                        lambda *a, **k: "fake_tokenizer")
    monkeypatch.setattr("transformers.TFDistilBertForSequenceClassification.from_pretrained",
                        lambda *a, **k: "fake_model")

def test_empty_input():
    msg, color = predictor.predict("")
    assert "Введите текст" in msg
    assert color == "orange"

def test_non_english_input():
    msg, color = predictor.predict("Привет, это письмо")
    assert "Введите текст" in msg
    assert color == "orange"

def test_api_error(monkeypatch):
    def fake_post(*args, **kwargs):
        raise Exception("API недоступно")
    monkeypatch.setattr(predictor.requests, "post", fake_post)
    msg, color = predictor.predict("Hello, world")
    assert "Ошибка при подключении" in msg
    assert color == "orange"

def test_api_success_phishing(monkeypatch):
    class FakeResponse:
        def json(self):
            return {"label": "phishing", "response_score": 0.95}
    monkeypatch.setattr(predictor.requests, "post", lambda *a, **k: FakeResponse())
    msg, color = predictor.predict("Hello, I am a prince, send me money")
    assert "Фишинговое письмо" in msg
    assert color == "red"

def test_api_success_safe(monkeypatch):
    class FakeResponse:
        def json(self):
            return {"label": "safe", "response_score": 0.88}
    monkeypatch.setattr(predictor.requests, "post", lambda *a, **k: FakeResponse())
    msg, color = predictor.predict("Hello, this is a normal email")
    assert "Безопасное письмо" in msg
    assert color == "green"