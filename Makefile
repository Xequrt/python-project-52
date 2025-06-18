build:
	./build.sh
render-start:
	gunicorn task_manager.wsgi
install:
	uv sync

collectstatic:
	uv run python3 manage.py collectstatic --noinput

compilemessages:
	uv run django-admin compilemessages

migrate:
	uv run python3 manage.py migrate

start:
	uv run manage.py runserver 0.0.0.0:8000

test:
	uv run python3 manage.py test

lint:
	uv run ruff check .