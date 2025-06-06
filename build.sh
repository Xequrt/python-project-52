#!/usr/bin/env bash
# скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# здесь добавьте все необходимые команды для установки вашего проекта
# команду установки зависимостей, сборки статики, применения миграций и другие
make install && make collectstatic && make migrate

SUPERUSER_EXISTS=$(python3 manage.py shell -c \
"from django.contrib.auth.models import User; \
print(User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists())")

if [ "$SUPERUSER_EXISTS" = "False" ]; then
    uv run python3 manage.py createsuperuser \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL \
        --noinput
fi