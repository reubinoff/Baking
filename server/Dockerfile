FROM python:3.12-slim

ARG USER=baking
ARG WORKDIR=/app/

WORKDIR $WORKDIR

RUN groupadd -f -g 1000 $USER && useradd -m $USER --gid 1000 && chown -R $USER:$USER $WORKDIR

# Install Poetry
RUN apt-get update
RUN apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY --chown=$USER:$USER ./pyproject.toml ./poetry.lock* $WORKDIR

RUN poetry install --no-root --only main

COPY --chown=$USER:$USER src/ .
COPY --chown=$USER:$USER scripts/prestart.sh .

# FastApi Configuration
ENV WORKERS_PER_CORE=1
ENV MAX_WORKERS=1

RUN apt-get clean && apt-get autoclean

CMD ["fastapi", "run", "baking/main.py", "--port", "8000"]
