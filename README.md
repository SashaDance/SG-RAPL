<p align="center">

  <h1 align="center">SG-RAPL: <br>
Scene Graph-Driven Reasoning <br> for Action Planning of Humanoid Robot</h1>
  <p align="center">
    Yudin Dmitry
    ·
    Kochetkova Angelika
    .
    Bakaeva Eva
    <br>
    Lazarev Aleksandr
    ·
    Panov Aleksandr
    .
    Kovalev Aleksei
    ·
  </p>

  <h4 align="center"><a href="https://sashadance.github.io/SG-RAPL.github.io/">Project</a> | <a href="http://arxiv.org/abs/xxxx.xxxx">arXiv</a> | <a href="https://github.com/SashaDance/SG-RAPL">Code</a></h4>
  <div align="center"></div>
</p>

<p align="center">
<img src="smth.png" width="80%">
</p>

# Launch 
This project follows a microservice architecture, microservices communicate with each other with volumes.

## Run a service
```bash

docker compose up -d --build
export COMPOSE_FILE=compose.base.yaml:compose.dev.yaml
docker compose up -d --build $SERVICE
```

## Test service


```bash
export COMPOSE_FILE=compose.base.yaml:compose.dev.yaml
docker compose up -d --build $SERVICE
docker compose exec $SERVICE bash -c "poetry run pytest -vv"
```

## Bare requests
To a service by `curl`
```bash
curl --location --request POST 'http://service:8000/invoke' \
    --header 'Content-Type: application/json' \
    --data-raw '{}'
```