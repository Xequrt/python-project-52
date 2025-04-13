build:
	./build.sh
render-start:
	uv run gunicorn task_manager.wsgi
install:
	uv sync

collectstatic:
	python3 manage.py collectstatic --noinput

migrate:
	python3 manage.py migrate

run:
	python3 manage.py runserver
