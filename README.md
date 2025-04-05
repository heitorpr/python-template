# setup uv

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh

# windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

# setup venv

```shell
uv venv
.\.venv\Scripts\activate.ps1
uv sync
```

# build image

```shell
docker build --target=production . -t python_template
```

# run project

```shell
docker compose up -d --build

# remove project
docker compose --profile '*' down

# run project with debug
docker compose --profile 'debug' up -d --build
```

# migrations

```shell
# run migrations
docker compose exec -it app alembic upgrade head

# create migrations
docker compose exec -it app alembic revision --autogenerate -m "my awesome comment"
```

# lint and format

```shell
# verify and fix linting issues
ruff check . --fix

# format all files
ruff format .
```

# setup pre-commit

```shell
pre-commit install -f
pre-commit install --hook-type commit-msg
```

# tests

```shell
# Run all tests
pytest

# Run stress tests
locust -f .\scripts\locust\locustfile.py
```
