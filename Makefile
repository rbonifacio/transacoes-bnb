.PHONY: check format lint types test

check: lint types test

format:
	poetry run ruff format src tests

lint:
	poetry run ruff check src tests

types:
	poetry run mypy

test:
	poetry run pytest
