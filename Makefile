run:
	FLASK_APP=app \
	FLASK_DEBUG=1 \
	uv run flask run --host=0.0.0.0 --port=5000 --reload

ui:
	npx tailwindcss -i ./app/static/css/input.css -o ./app/static/css/tailwind.css --watch --minify

install:
	uv venv
	uv sync
	npm install
	uv run pre-commit install

lint:
	uv run ruff check .
	uv run ruff format --check .
	npx biome check .

format:
	uv run ruff check --fix .
	uv run ruff format .
	npx biome check --write .

.PHONY: run ui install lint format