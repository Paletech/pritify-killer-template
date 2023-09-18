FROM python:3.10

ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE 1

WORKDIR /src

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv
RUN pipenv install --system

COPY . .
