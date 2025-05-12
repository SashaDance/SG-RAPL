FROM python:3.10

ENV POETRY_VERSION=1.8.3 \ 
    POETRY_HOME="/opt/poetry"

ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app
# copy packages dirs 
COPY common_packages /common_packages
COPY services/actual_state/pyproject.toml services/actual_state/poetry.lock ./

RUN poetry lock
RUN poetry install

COPY services/actual_state/ .

CMD ["poetry", "run", "fastapi", "run"]
