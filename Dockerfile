FROM python:3.10-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Устанавливаем зависимости системы
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
RUN echo 123
# Создаем директорию для медиафайлов
RUN mkdir -p /app/media && chmod 777 /app/media
# Копируем оставшиеся файлы проекта
COPY . /app/

# Пробрасываем порт
EXPOSE 8011

# Команда запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8011"]
