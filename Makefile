run:
	FLASK_APP=app \
	FLASK_DEBUG=1 \
	. venv/bin/activate && flask run --host=0.0.0.0 --port=5000 --reload

ui:
	npx tailwindcss -i ./app/static/css/input.css -o ./app/static/css/tailwind.css --watch --minify

insall:
	python2 -m venv venv
	@echo "Installing python dependencies"
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	@echo "Setting up frontend dependencies..."
	npm install
	@echo "Setup complete. Activate venv with: . venv/bin/activate"
