# syntax=docker/dockerfile:1
FROM python:3.10

ENV POETRY_VERSION=1.8.3 \ 
    POETRY_HOME="/opt/poetry"

ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -


WORKDIR /app
# copy packages dirs 
COPY common_packages /common_packages
COPY services/planner/packages packages
# copy files
COPY services/planner/pyproject.toml services/planner/poetry.lock ./

RUN poetry install

# sync with all service data
COPY services/planner/ .

CMD ["poetry", "run", "fastapi", "run"]
