#FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime
FROM python:3.10

ENV POETRY_VERSION=1.8.3 \ 
    POETRY_HOME="/opt/poetry"

ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -


WORKDIR /app
# copy packages dirs 
COPY common_packages /common_packages

# copy files
COPY services/llm_vicuna13b/pyproject.toml services/llm_vicuna13b/poetry.lock ./

RUN poetry install

# sync with all service data
COPY services/llm_vicuna13b/ .

CMD ["poetry", "run", "fastapi", "run"]
