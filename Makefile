build:
	./build.sh
render-start:
	gunicorn task_manager.wsgi
install:
	uv sync

collectstatic:
	uv run python3 manage.py collectstatic --noinput

migrate:
	uv run python3 manage.py migrate

run:
	uv run python3 manage.py runserver

test:
	uv run python3 manage.py test

lint:
	uv run ruff check .