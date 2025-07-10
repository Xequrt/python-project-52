from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'executor', 'status', 'labels']
        widgets = {
            'executor': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'labels': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'multiple': True
            }),
        }