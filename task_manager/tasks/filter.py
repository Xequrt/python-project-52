import django_filters
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_('Status'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=get_user_model().objects.all(),
        label=_('Executor'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    is_author = django_filters.BooleanFilter(
        method='filter_by_author',
        label=_('Your tasks'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-label'})
    )

    def filter_by_author(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'is_author']