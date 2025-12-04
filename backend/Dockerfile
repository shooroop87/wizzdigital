FROM python:3.9-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1) зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) код проекта
COPY . .

# 3) каталог для статики + сбор статики при сборке образа
RUN mkdir -p /app/collected_static && \
    SECRET_KEY=build-time-secret python manage.py collectstatic --noinput

# 4) entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=3"]