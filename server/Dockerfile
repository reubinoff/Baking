FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10-slim

ARG USER=baking
ARG WORKDIR=/app/
ARG CERT_PATH=/etc/ssl/certs/sql-prod-baking.crt.pem
ARG CERT_LOCATION

WORKDIR $WORKDIR

RUN groupadd -f -g 1000 $USER && useradd -m $USER --gid 1000 && chown -R $USER:$USER $WORKDIR

# Install Poetry
RUN apt-get update
RUN apt-get install -y curl postgresql-client
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY --chown=$USER:$USER ./pyproject.toml ./poetry.lock* $WORKDIR

RUN poetry install --no-root --no-dev

COPY --chown=$USER:$USER src/ .
COPY --chown=$USER:$USER scripts/prestart.sh .

# FastApi Configuration
ENV service_name="baking-service"
ENV MODULE_NAME="baking.main"
ENV VARIABLE_NAME="app"
ENV WORKERS_PER_CORE=1
ENV MAX_WORKERS=1

RUN apt-get clean && apt-get autoclean