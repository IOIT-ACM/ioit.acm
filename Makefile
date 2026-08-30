run:
	FLASK_APP=app \
	FLASK_DEBUG=1 \
	. venv/bin/activate && flask run --host=0.0.0.0 --port=5000 --reload

ui:
	npx tailwindcss -i ./app/static/css/input.css -o ./app/static/css/tailwind.css --watch --minify

install:
	/home/krishna/.local/bin/uv venv
	/home/krishna/.local/bin/uv sync

.PHONY: run ui install