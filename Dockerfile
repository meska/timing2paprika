FROM python:3.11
LABEL authors="meska"

WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

COPY . /app
CMD ["python", "main.py"]