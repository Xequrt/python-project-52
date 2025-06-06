build:
	./build.sh
render-start:
	gunicorn task_manager.wsgi
install:
	uv sync

collectstatic:
	python3 manage.py collectstatic --noinput

migrate:
	python3 manage.py migrate

run:
	python3 manage.py runserver

test:
	python3 manage.py test

lint:
	uv run ruff check .