.PHONY: up down logs rebuild test lint typecheck build check

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

rebuild:
	docker compose build --no-cache

test:
	docker compose run --rm api sh -c "pip install '.[dev]' >/dev/null && pytest -q"

lint:
	docker compose run --rm api sh -c "pip install '.[dev]' >/dev/null && ruff check . && ruff format --check ."

typecheck:
	docker compose run --rm web npm run typecheck

build:
	docker compose build

check: test lint typecheck build

