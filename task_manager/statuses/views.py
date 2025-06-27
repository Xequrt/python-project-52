from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, render
from .models import Status
from .forms import StatusForm


class StatusesListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses_list.html'
    context_object_name = 'statuses'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return super().get_queryset().order_by('name')


class StatusesCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = StatusForm
    template_name = 'statuses/status_create.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _("Status created successfully!")
    login_url = reverse_lazy('login')


    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return response
        except IntegrityError:
            messages.error(self.request, _("Status with this name already exists"))
            return self.render_to_response(self.get_context_data(form=form))


class StatusesUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_update.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _("Status updated successfully!")
    login_url = reverse_lazy('login')

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Status, pk=self.kwargs.get('pk'))



    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return response
        except IntegrityError:
            messages.error(self.request, _("Status with this name already exists"))
            return self.render_to_response(self.get_context_data(form=form))


class StatusesDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_confirm_delete.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _("Status deleted successfully!")
    login_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return get_object_or_404(Status, pk=self.kwargs.get('pk'))


    def delete(self, request, *args, **kwargs):
        if self.object.task_set.exists():
            messages.warning(self.request, _("This status is currently in use and cannot be deleted"))
            return HttpResponseRedirect(self.get_success_url())

        try:
            return super().delete(request, *args, **kwargs)
        except IntegrityError:
            messages.error(self.request, _("Failed to delete status."))
            return render(self.request, self.template_name, self.get_context_data())
