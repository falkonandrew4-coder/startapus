FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Програмний продукт розроблено Соколом Андрієм - Falkon AI
# Використовуємо shell form для підтримки $PORT від Railway
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
