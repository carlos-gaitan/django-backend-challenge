# syntax=docker/dockerfile:1
FROM python:3.7

ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  PIPENV_HIDE_EMOJIS=true \
  PIPENV_COLORBLIND=true \
  PIPENV_NOSPIN=true \
  PIPENV_DOTENV_LOCATION=config/.env

# Creating folders, and files for a project:
WORKDIR /code
COPY . /code/

# Project initialization:
RUN pip install pipenv
RUN cd /code
RUN pipenv install --system --deploy --ignore-pipfile
RUN python manage.py migrate
RUN python manage.py import_books