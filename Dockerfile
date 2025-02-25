FROM python:3.13-slim

EXPOSE 6177

WORKDIR /sevice

RUN pip install poetry

COPY ./pyproject.toml .

RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-interaction --no-ansi --no-root

COPY ./alembic.ini .

COPY /app ./app

CMD ["sh", "-c", "alembic upgrade head && python ./app/start.py"]