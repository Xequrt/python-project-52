from django.db import models
from django.utils.translation import gettext_lazy as _

class Label(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=100,
        unique=True,
        help_text=_('Unique label name'),
        error_messages={
            'unique': _('Label with this name already exists'),
        }
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')
        ordering = ['name']

    def __str__(self):
        return self.name
