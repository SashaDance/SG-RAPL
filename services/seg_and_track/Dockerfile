FROM pytorch/pytorch:2.4.1-cuda11.8-cudnn9-runtime
FROM python:3.10.0

RUN apt-get update && \
    apt-get install -y curl libgl1-mesa-glx libglib2.0-0 libsm6 libxrender1 libxext6 && \
    rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.8.3 \ 
    POETRY_HOME="/opt/poetry"

ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app
# copy packages dirs
COPY common_packages /common_packages
# copy files
COPY services/seg_and_track/pyproject.toml services/seg_and_track/poetry.lock ./

# RUN poetry lock && poetry install
RUN poetry install

# # sync with all service data
COPY services/seg_and_track/ .

CMD ["poetry", "run", "fastapi", "run"]
