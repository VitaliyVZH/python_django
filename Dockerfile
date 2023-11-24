# базовый образ
FROM python:3.10.0

# отключение буферизации
ENV PYTHONUNBUFFERED=1

# директория для установки приложения
WORKDIR /app

# обновление poetry
RUN pip install --upgrade pip "poetry==1.7.0"

# отключение автоматического создания poetry виртуальной среды (--local - для текущего проекта)
RUN poetry config virtualenvs.create false --local


COPY pyproject.toml poetry.lock ./
RUN poetry install

# копирование файлов в директорию
COPY mysite .

CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]