from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=100,
        unique=True,
        help_text=_('Unique task name'),
        error_messages={
            'unique': _('Task with this name already exists'),
        }

    )
    description = models.TextField(
        _('Description'),
        blank=True,
        max_length=500,
        help_text=_('Detailed task description')
    )

    executor = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='executor_tasks',
        verbose_name=_('Executor'),
        help_text=_('User responsible for the task')
    )

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='created_tasks',
        verbose_name=_('Author'),
        help_text=_('User who created the task')
    )

    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_('Status'),
        help_text=_('Current task status')
    )

    labels = models.ManyToManyField(
        Label,
        blank=True,
        verbose_name=_('Labels'),
        help_text=_('Current task label')
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ['name']

    def __str__(self):
        return self.name
