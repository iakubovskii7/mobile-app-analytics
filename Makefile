.PHONY: format lint activate tests clean

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

IMAGE_NAME = mobile_engineering
IMAGE_TAG = dev
PY_IMAGE = python
PY_IMAGE_VERSION = 3.12-slim

CODE = src
MANAGER = poetry run
LINT = src

DATE_START = $(shell TZ='Europe/Tbilisi' date +%Y-%m-%d)

activate:
	poetry install -vvv --with=tests,linters

format: # Formats all files
	$(MANAGER) ruff check --select I --fix $(CODE)
	$(MANAGER) ruff format $(CODE)

lint: # Lint code
	$(MANAGER) ruff format --diff $(CODE)
	$(MANAGER) ruff check $(CODE)
	$(MANAGER) mypy $(LINT)

tests:
	docker-compose up -d spark-master spark-worker-1
	docker-compose up pytest-runner-demand-forecast --build

clean:
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .coverage
	rm -rf .coverage.*
	rm -rf __pycache