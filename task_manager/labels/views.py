from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, render, redirect
from .models import Label
from .forms import LabelForm


class LabelsListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels_list.html'
    context_object_name = 'labels'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return super().get_queryset().order_by('name')


class LabelsCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = LabelForm
    template_name = 'labels/label_create.html'
    success_url = reverse_lazy('labels_list')
    success_message = _("Label created successfully!")
    login_url = reverse_lazy('login')


    def form_valid(self, form):
        try:
            form.instance.name = form.cleaned_data['name']
            response = super().form_valid(form)
            return response
        except IntegrityError:
            messages.error(self.request, _("Label with this name already exists"))
            return self.render_to_response(self.get_context_data(form=form))


class LabelsUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_update.html'
    success_url = reverse_lazy('labels_list')
    success_message = _("Label updated successfully!")
    login_url = reverse_lazy('login')

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Label, pk=self.kwargs.get('pk'))

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if not request.user.is_superuser and obj != request.user:
            messages.error(request, _("You can only update your own label"))
            return redirect('labels_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return response
        except IntegrityError:
            messages.error(self.request, _("Label with this name already exists"))
            return self.render_to_response(self.get_context_data(form=form))


class LabelsDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/label_confirm_delete.html'
    success_url = reverse_lazy('labels_list')
    success_message = "Label deleted successfully!"
    login_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return get_object_or_404(Label, pk=self.kwargs.get('pk'))

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if not request.user.is_superuser and obj != request.user:
            messages.error(request, _("You can only delete your own label"))
            return redirect('labels_list')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if self.object.task_set.exists():
            messages.warning(self.request, _("This label is currently in use and cannot be deleted"))
            return HttpResponseRedirect(self.get_success_url())

        try:
            return super().delete(request, *args, **kwargs)
        except IntegrityError:
            messages.error(self.request, _("Failed to delete label"))
            return render(self.request, self.template_name, self.get_context_data())
