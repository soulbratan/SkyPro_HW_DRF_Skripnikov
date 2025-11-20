FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE=False

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]