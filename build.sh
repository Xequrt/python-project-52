#!/usr/bin/env bash
# скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# здесь добавьте все необходимые команды для установки вашего проекта
# команду установки зависимостей, сборки статики, применения миграций и другие
make install && make collectstatic && make migrate

uv run python3 manage.py migrate --noinput
uv run python3 manage.py createsuperuser \
    --username $DJANGO_SUPERUSER_USERNAME \
    --email $DJANGO_SUPERUSER_EMAIL \
    --noinput