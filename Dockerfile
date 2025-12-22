FROM python:3.11-slim

WORKDIR /app

# Встановлюємо системні залежності
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо та встановлюємо Python-залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь проєкт
COPY . .

# Збираємо статику та застосовуємо міграції
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --noinput

# Використовуємо Gunicorn для продакшену
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "config.wsgi:application"]
