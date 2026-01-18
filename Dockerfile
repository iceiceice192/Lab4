# Используем легкий образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем переменные окружения для Python (чтобы не создавал pyc файлы и выводил логи сразу)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем зависимости системы (нужно для psycopg2 иногда, но в slim-версии binary работает и так)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем библиотеки Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта внутрь контейнера
COPY . .

# Собираем статические файлы (CSS, JS) в одну папку
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Команда, которая запустится при старте контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]