
.PHONY: setup test

setup:
	pre-commit install
	poetry install

lint:
	poetry run isort .
	poetry run black weathery tests

test: setup lint
	poetry run pytest --cov xml:cov.xml
