# Generated by Django 5.2 on 2025-05-28 08:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("statuses", "0003_alter_status_created_at"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        error_messages={"unique": "Task with this name already exists"},
                        help_text="Unique task name",
                        max_length=100,
                        unique=True,
                        verbose_name="Name",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Detailed task description",
                        max_length=500,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "executor",
                    models.ForeignKey(
                        help_text="User responsible for the task",
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Executor",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        help_text="Current task status",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="statuses.status",
                        verbose_name="Status",
                    ),
                ),
            ],
            options={
                "verbose_name": "Task",
                "verbose_name_plural": "Tasks",
                "ordering": ["name"],
            },
        ),
    ]
