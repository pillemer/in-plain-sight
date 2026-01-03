.PHONY: dev test lint format install

dev:
	poetry run uvicorn app.main:app --reload

test:
	poetry run pytest -v

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

install:
	poetry install

seed:
	poetry run python -m app.seed