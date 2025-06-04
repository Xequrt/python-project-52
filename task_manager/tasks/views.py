from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, render, redirect
from .models import Task
from .forms import TaskForm
from django_filters.views import FilterView
from .filter import TaskFilter


class TasksListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/tasks_list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return super().get_queryset().order_by('name')


class TaskView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_view.html'
    context_object_name = 'task'
    login_url = reverse_lazy('login')

class TasksCreateView(SuccessMessageMixin, CreateView):
    form_class = TaskForm
    template_name = 'tasks/tasks_create.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _("Task created successfully!")


    def form_valid(self, form):
        try:
            form.instance.author = self.request.user
            response = super().form_valid(form)
            return response
        except IntegrityError:
            messages.error(self.request, _("Task with this name already exists"))
            return self.render_to_response(self.get_context_data(form=form))


class TasksUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/tasks_update.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _("Task updated successfully!")
    login_url = reverse_lazy('login')

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Task, pk=self.kwargs.get('pk'))

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if not request.user.is_superuser and obj.author != request.user:
            messages.error(request, _("You can only update your own task"))
            return redirect('tasks_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return response
        except IntegrityError:
            messages.error(self.request, _("Task with this name already exists"))
            return self.render_to_response(self.get_context_data(form=form))


class TasksDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/tasks_confirm_delete.html'
    success_url = reverse_lazy('tasks_list')
    success_message = "Task deleted successfully!"
    login_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return get_object_or_404(Task, pk=self.kwargs.get('pk'))

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if not request.user.is_superuser and obj.author != request.user:
            messages.error(request, _("You can only delete your own task"))
            return redirect('tasks_list')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if self.object.task_set.exists():
            messages.warning(self.request, _("This task is currently in use and cannot be deleted"))
            return HttpResponseRedirect(self.get_success_url())

        try:
            return super().delete(request, *args, **kwargs)
        except IntegrityError:
            messages.error(self.request, _("Failed to delete task."))
            return render(self.request, self.template_name, self.get_context_data())
