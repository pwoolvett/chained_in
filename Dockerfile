FROM python:3.6-alpine

MAINTAINER Pablo Woolvett <pablowoolvett@gmail.com>

# Install system dependencies here
RUN "curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python"

# avoid virtualenvs in production, see https://github.com/sdispater/poetry/issues/218
RUN "poetry config settings.virtualenvs.create false"

# Add poetry.lock before rest of repo for caching, see https://www.aptible.com/documentation/enclave/tutorials/faq/dockerfile-caching/pip-dockerfile-caching.html
ADD poetry.lock /app/
ADD pyproject.toml /app/

WORKDIR /app
RUN "poetry install --no-dev -v"

ADD . /app

CMD python3 chained_in
