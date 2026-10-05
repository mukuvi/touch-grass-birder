.PHONY: setup models run test lint clean

setup:
	uv sync --extra dev

models:
	bash scripts/download_gemma.sh

run:
	uv run uvicorn app.main:app --host 127.0.0.1 --port 8000

test:
	uv run pytest -q

lint:
	uv run ruff check .

clean:
	rm -rf data models .venv __pycache__ .pytest_cache
