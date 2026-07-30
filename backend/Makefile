.PHONY: install run test lint format typecheck test-cov migrate generate-migration help

install:
	poetry install

run:
	poetry run uvicorn core.server:app --reload --host 0.0.0.0 --port 8000

migrate:
	poetry run alembic upgrade head

generate-migration:
	poetry run alembic revision --autogenerate -m "$(MSG)"

test:
	poetry run pytest

test-cov:
	poetry run pytest --cov=. --cov-report=html --cov-report=term-missing

lint:
	poetry run ruff check .
	poetry run ruff format --check .

format:
	poetry run ruff format .
	poetry run ruff check --fix .

typecheck:
	poetry run mypy .

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
