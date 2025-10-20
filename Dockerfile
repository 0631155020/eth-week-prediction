# Использование официального образа Python
FROM python:3.10-slim

# Установка зависимостей, необходимых для pystan/prophet
RUN apt-get update && \
    apt-get install -y build-essential gcc gfortran python3-dev

# Установка рабочей директории
WORKDIR /app

# Копирование файла с зависимостями и установка
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . /app

# Определение команды, которая будет запускаться при старте контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
