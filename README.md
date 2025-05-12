# Planner module
### Run a service
```bash

docker compose up -d --build
export COMPOSE_FILE=compose.base.yaml:compose.dev.yaml
docker compose up -d --build $SERVICE
```

### Test service

planner or llm_vicuna13b

```bash
export COMPOSE_FILE=compose.base.yaml:compose.dev.yaml
# set -x COMPOSE_FILE compose.base.yaml:compose.dev.yaml
docker compose up -d --build $SERVICE
docker compose exec $SERVICE bash -c "poetry run pytest -vv"
# or with stdout `docker compose exec $SERVICE bash -c "poetry run pytest -vv  --capture=tee-sys"`
```



#### Bare requests
To a service by `curl`
```bash
curl --location --request POST 'http://service:8000/invoke' \
    --header 'Content-Type: application/json' \
    --data-raw '{}'
```
![Demo](/demo/demo.webm)