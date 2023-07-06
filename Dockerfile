FROM python:3.11

RUN apt update && apt upgrade -y

RUN pip install -U pip && pip install poetry

WORKDIR /tele-gpt

COPY pyproject.toml .

RUN poetry install --no-root

COPY . .

CMD poetry run python -m tele-gpt
