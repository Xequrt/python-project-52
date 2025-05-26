from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        labels = {
            'name': _('Name'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Status.objects.exclude(pk=self.instance.pk).filter(name=name).exists():
            raise ValidationError(_('Status with this name already exists'))
        return name
