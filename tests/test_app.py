import pytest
from streamlit.app import predict

# Ввод пустого запроса
def test_predict_empty_text():
    message, color = predict("")
    assert "Введите" in message
    assert color == "orange"

# Ввод текста не на английском языке
def test_predict_non_english_text():
    message, color = predict("Это письмо на русском языке.")
    assert "Введите" in message
    assert color == "orange"

# Ввод цифр
def test_predict_numbers_only():
    message, color = predict("1234567890")
    assert "Введите" in message
    assert color == "orange"

# Ввод спец. символов
def test_predict_special_characters():
    message, color = predict("!!!@@@###$$$")
    assert "Введите" in message
    assert color == "orange"

# Смешанный ввод
def test_predict_mixed_symbols_and_letters():
    message, color = predict("Click here!!! $$$ Save now 123")
    assert "письмо" in message
    assert color in ["red", "green"]

# Безопасное письмо
def test_predict_safe_email():
    message, color = predict("Hello, your meeting is confirmed for tomorrow at 10 AM.")
    assert "Безопасное" in message
    assert color == "green"

# Фишинговое письмо
def test_predict_phishing_email():
    phishing_text = "Your account has been suspended. Click here to verify your login immediately."
    message, color = predict(phishing_text)
    assert "Фишинговое" in message

    assert color == "red"
