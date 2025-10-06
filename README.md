# 📧 Phishing Detector
Приложение для определения фишинговых писем с помощью модели DistilBERT.
Проект включает FastAPI, Streamlit-интерфейс, Docker и тесты с Pytest.

## Возможности
* Анализ текста письма на английском языке
* Предобработка текста
* Модель DistilBERT
* Уровень уверенности модели
* Streamlit-интерфейс для визуального ввода
* API на FastAPI
* Docker и docker-compose для запуска

![Streamlit-интерфейс](screenshots/streamlit.png)

## Стек технологий
* Python 3.10
* Transformers (DistilBERT)
* TensorFlow
* NLTK
* FastAPI
* Streamlit
* Docker
* Pytest
* GitHub Actions

## Обучение модели
Процесс обучения этой модели (а также LSTM и Logistic regression) и данные, на которых обучались модели, представлены в **/model_training**

## Запуск проекта c Docker
```
docker-compose up --build
```
FastAPI: http://localhost:8000/docs

Streamlit: http://localhost:8501

## Запуск без Docker
```
pip install -r api/requirements.txt
pip install -r streamlit/requirements.txt

uvicorn api.api:app --reload

streamlit run streamlit/app.py
```
