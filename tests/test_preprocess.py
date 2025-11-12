import re
import pytest
from ui.preprocess import (to_lowercase,
                        expand_contractions,
                        remove_html,
                        remove_urls,
                        remove_emails,
                        remove_numbers,
                        remove_special_chars,
                        tokenize_and_lemmatize,
                        remove_duplicates,
                        clean_text)

# Замена множественных пробелов на один и приведение к нижнему регистру
def normalize_spaces(text: str) -> str:
    import re
    return re.sub(r"\s+", " ", text).strip().lower()

@pytest.mark.parametrize("inp, expected", [("HELLO World", "hello world"),
                                           ("Python", "python")])
# Проверяем приведение к нижнем регистру
def test_to_lowercase(inp, expected):
    assert to_lowercase(inp) == expected

@pytest.mark.parametrize("inp, expected_substr", [("I can't do this", "cannot"),
                                                  ("You're amazing", "you are")])
# Проверяем расширение сокращений
def test_expand_contractions(inp, expected_substr):
    result = expand_contractions(inp).lower()
    assert expected_substr in result

@pytest.mark.parametrize("inp, forbidden", [("<p>Hello</p>", "<p>"),
                                            ("<div>World</div>", "<div>")])
# Проверяем удаление HTML-тегов
def test_remove_html(inp, forbidden):
    result = remove_html(inp).lower()
    assert forbidden not in result

@pytest.mark.parametrize("inp", ["Check http://example.com please",
                                 "Visit www.test.com now"])
# Проверяем удаление URL-адресов
def test_remove_urls(inp):
    result = remove_urls(inp).lower()
    assert "http" not in result and "www" not in result

@pytest.mark.parametrize("inp", ["Contact me at test@mail.com",
                                 "Send to hello@domain.org"])
# Проверяем удаление email-адресов
def test_remove_emails(inp):
    result = remove_emails(inp)
    assert "@" not in result

@pytest.mark.parametrize("inp, expected", [("I have 2 apples", "i have apples"),
                                           ("123 numbers removed", "numbers removed")])
# Проверяем удаление чисел
def test_remove_numbers(inp, expected):
    result = normalize_spaces(remove_numbers(inp))
    assert result == expected

@pytest.mark.parametrize("inp, expected_word", [("Hello!!! $$$", "hello"),
                                                ("Python###", "python")])
# Проверяем удаление специальных символов
def test_remove_special_chars(inp, expected_word):
    result = normalize_spaces(remove_special_chars(inp))
    assert expected_word in result

@pytest.mark.parametrize("inp, expected_tokens", [("cats dogs running", {"cat", "dog"}),
                                                  ("better houses", {"better", "house"})])
# Проверка токенизации и лемматизации
def test_tokenize_and_lemmatize(inp, expected_tokens):
    tokens = set(tokenize_and_lemmatize(inp))
    assert expected_tokens.issubset(tokens)

@pytest.mark.parametrize("inp, expected", [(["hello", "hello", "world"], ["hello", "world"]),
                                           (["a", "a", "a"], ["a"])])
# Проверяем удаление дубликатов
def test_remove_duplicates(inp, expected):
    assert remove_duplicates(inp) == expected

# Проверяем последовательность вызова clean_text
def test_clean_text_pipeline():
    text = "I can't believe it's 2025!!! <b>Hello</b> world..."
    cleaned = normalize_spaces(clean_text(text))
    assert "cannot" in cleaned
    assert "hello" in cleaned
    assert "2025" not in cleaned

# Проверяем работу функции clean_text
def test_integration_clean_text():
    raw_text = """<html>
                        <body>
                            I can't believe it's already 2025!!!
                            Contact me at test@mail.com or visit http://example.com
                            <b>Hello</b> WORLD!!!
                        </body>
                    </html>"""
    cleaned = normalize_spaces(clean_text(raw_text))
    assert "cannot" in cleaned
    assert "hello" in cleaned
    assert "world" in cleaned
    assert "2025" not in cleaned
    assert "@" not in cleaned
    assert "http" not in cleaned
