FROM python:3.11

ENV PYTHONBUFFERED=1

ENV POETRY_VERSION=1.7.1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /src

RUN apt-get update  \
    && apt-get install -y --no-install-recommends gunicorn  \
    && apt-get clean  \
    && rm -rf /var/lib/apt/lists/*  \
    && pip install --no-cache-dir --upgrade pip

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv
RUN pipenv install --system
COPY . ./

COPY run_app.sh .
RUN mkdir -p /src/staticfiles

ENTRYPOINT ["/bin/bash", "/src/run_app.sh"] 
