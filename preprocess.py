import re
from typing import List, Callable
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("punkt", quiet=True)

STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()

CONTRACTIONS = {"can't": "cannot",
                "won't": "will not",
                "i'm": "i am",
                "it's": "it is",
                "don't": "do not",
                "didn't": "did not",
                "doesn't": "does not",
                "you're": "you are",
                "they're": "they are",
                "we're": "we are",
                "i've": "i have",
                "isn't": "is not",
                "aren't": "are not",
                "wasn't": "was not",
                "weren't": "were not",
                "hasn't": "has not",
                "haven't": "have not",
                "hadn't": "had not",
                "wouldn't": "would not",
                "shouldn't": "should not",
                "couldn't": "could not",
                "mustn't": "must not"}

def to_lowercase(text: str) -> str:
    return text.lower()

def expand_contractions(text: str) -> str:
    for word, expanded in CONTRACTIONS.items():
        text = re.sub(r"\b" + word + r"\b", expanded, text, flags=re.IGNORECASE)
    return text

def remove_html(text: str) -> str:
    return re.sub(r"<.*?>", " ", text)

def remove_urls(text: str) -> str:
    return re.sub(r"http\S+|www\S+", " ", text)

def remove_emails(text: str) -> str:
    return re.sub(r"\S+@\S+", " ", text)

def remove_numbers(text: str) -> str:
    text = re.sub(r"\d+", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def remove_special_chars(text: str) -> str:
    return re.sub(r"[^a-zA-Z\s]", " ", text)

def tokenize_and_lemmatize(text: str) -> List[str]:
    tokens = text.split()
    return [LEMMATIZER.lemmatize(w) for w in tokens if w not in STOP_WORDS]

def remove_duplicates(tokens: List[str]) -> List[str]:
    cleaned = []
    for w in tokens:
        if not cleaned or w != cleaned[-1]:
            cleaned.append(w)
    return cleaned

def clean_text(text: str) -> str:
    text = to_lowercase(text)
    text = expand_contractions(text)
    text = remove_html(text)
    text = remove_urls(text)
    text = remove_emails(text)
    text = remove_numbers(text)
    text = remove_special_chars(text)

    tokens = tokenize_and_lemmatize(text)
    tokens = remove_duplicates(tokens)

    return " ".join(tokens)