FROM python:3.10

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
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем оставшиеся файлы проекта
COPY . /app/

# Пробрасываем порт
EXPOSE 8001

# Команда запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
