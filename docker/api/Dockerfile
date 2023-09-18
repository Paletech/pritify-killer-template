FROM python:3.10

ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE 1

WORKDIR /src

COPY Pipfile Pipfile.lock ./

RUN apt-get update && apt-get install -y libglu1-mesa-dev
RUN pip install pipenv
RUN pipenv install --system

COPY . .
