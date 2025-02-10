dev:
	uv run flask --debug --app page_analyzer:app run

routes:
	uv run flask routes

install:
	uv sync

test:
	uv run pytest

lint:
	uv run ruff check

check: test lint

build:
	uv build
