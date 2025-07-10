from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        labels = {
            'name': _('Name'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Label.objects.exclude(
            pk=self.instance.pk
        ).filter(
            name=name
        ).exists():
            raise ValidationError(_('Label with this name already exists'))
        return name
