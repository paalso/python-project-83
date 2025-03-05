PORT ?= 8000

install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer:app run

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh

psql-connect:
	psql -U postgres -h localhost -d test -W

routes:
	uv run flask routes

test:
	uv run pytest

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

requirements:
	sed -n '/dependencies = \[/,/\]/p' pyproject.toml | grep -o '"[^"]\+"' | tr -d '"' > requirements.txt

check: test lint
