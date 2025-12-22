FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Змінні оточення для збірки (якщо потрібно)
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_HOST=db
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=postgres

# Збір статики (тепер без помилок з базою даних)
RUN python manage.py collectstatic --noinput

# Міграції застосовуються вже на етапі деплою, а не збірки
# RUN python manage.py migrate --noinput

EXPOSE $PORT

CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "config.wsgi:application"]
