from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'executor', 'status', 'labels']
        widgets = {
            'executor': forms.Select(attrs={'class': 'form-control bg-secondary bg-opacity-50 border-secondary'}),
            'status': forms.Select(attrs={'class': 'form-select bg-secondary bg-opacity-50 border-secondary'}),
            'labels': forms.SelectMultiple(attrs={
                'class': 'form-select bg-secondary bg-opacity-50 border-secondary',
                'multiple': True
            }),
        }