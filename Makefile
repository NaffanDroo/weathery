
.PHONY: setup test

setup:
	pre-commit install
	poetry install

test: setup
	poetry run pytest --cov xml:cov.xml
