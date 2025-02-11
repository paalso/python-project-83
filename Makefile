PORT ?= 8000

install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer:app run

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

render-start:
	# Install gunicorn if not already installed
	pip show gunicorn || pip install gunicorn
	# Start the application with gunicorn using the full path
	/opt/render/.local/bin/gunicorn --version
	/opt/render/.local/bin/gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh

routes:
	uv run flask routes

test:
	uv run pytest

lint:
	uv run ruff check

check: test lint
