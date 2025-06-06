# Default port for dev server
PORT ?= 8000

# ---------------------------------------------------------------------
# 🛠 Setup
# ---------------------------------------------------------------------

install:
	uv sync

build:
	./build.sh

requirements:
	# Extract dependencies from pyproject.toml to requirements.txt
	sed -n '/dependencies = \[/,/\]/p' pyproject.toml | grep -o '"[^"]\+"' | tr -d '"' > requirements.txt

# ---------------------------------------------------------------------
# 🚀 Development and Run
# ---------------------------------------------------------------------

dev:
	uv run python3 -m flask --app page_analyzer:app run --port=$(PORT)

start:
	uv run python3 -m gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

routes:
	uv run python3 -m flask --app page_analyzer:app routes

shell:
	uv run python3

# ---------------------------------------------------------------------
# 🧪 Tests and Lint
# ---------------------------------------------------------------------

test:
	uv run pytest

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

check: test lint

# ---------------------------------------------------------------------
# 🗃️ Database
# ---------------------------------------------------------------------

psql:
	psql -U postgres -h localhost -d test -W

# ---------------------------------------------------------------------
# ℹ️ Help
# ---------------------------------------------------------------------

help:
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "🛠  Setup:"
	@echo "  install        Install dependencies with uv"
	@echo "  build          Run build script (install deps + init DB)"
	@echo "  requirements   Export deps from pyproject.toml to requirements.txt"
	@echo ""
	@echo "🚀 Development and Run:"
	@echo "  dev            Run Flask dev server on port $(PORT)"
	@echo "  start          Start app with Gunicorn via uv"
	@echo "  render-start   Start app with Gunicorn directly"
	@echo "  routes         Show Flask route mappings"
	@echo "  shell          Start Python shell with project env"
	@echo ""
	@echo "🧪 Tests and Lint:"
	@echo "  test           Run tests with pytest"
	@echo "  lint           Run linter (ruff)"
	@echo "  lint-fix       Run linter with autofix"
	@echo "  check          Run tests and linter"
	@echo ""
	@echo "🗃️  Database:"
	@echo "  psql           Open psql to local 'test' database"
	@echo ""


.PHONY: install build requirements dev start render-start routes shell test lint lint-fix check psql help
