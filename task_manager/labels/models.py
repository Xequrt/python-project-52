from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.deletion import ProtectedError


class Label(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=100,
        blank=False,
        unique=True,
        help_text=_('Unique label name'),
        error_messages={
            'unique': _('Label with this name already exists'),
        }
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        """Prevent deletion if label is assigned to any tasks."""
        if self.task_set.exists():
            raise ProtectedError(
                _("Cannot delete this label because they are being used"),
                self
            )
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')
