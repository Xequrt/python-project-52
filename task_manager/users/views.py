from django.db.models import ProtectedError
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from .forms import CustomUserForm
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class UserListView(ListView):
    model = get_user_model()
    template_name = 'users/users_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return super().get_queryset().order_by('username')


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = CustomUserForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('login')
    success_message = _("User created successfully!")
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = False
        return context

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return response
        except IntegrityError:
            messages.error(self.request, _("User with this username already exists."))
            return self.render_to_response(self.get_context_data(form=form))


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('users_list')
    success_message = _("User updated successfully!")
    login_url = _url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context

    def get_object(self, *args, **kwargs):
        return get_object_or_404(get_user_model(), pk=self.kwargs.get('pk'))

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if not request.user.is_superuser and obj != request.user:
            messages.error(request, _("You do not have permission to modify another user."))
            return redirect('users_list')

        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = get_user_model()
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users_list')
    success_message = _("User deleted successfully!")
    login_url = _url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return get_object_or_404(get_user_model(), pk=self.kwargs.get('pk'))

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if not request.user.is_superuser and obj != request.user:
            messages.error(request, _("You can only delete your own account."))
            return redirect('users_list')

        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if self.object.task_set.exists():
            messages.warning(request, _("This user is currently assigned to tasks and cannot be deleted"))
            return HttpResponseRedirect(self.get_success_url())

        if self.object == request.user:
            messages.warning(request, _("You cannot delete your own account"))
            return HttpResponseRedirect(self.get_success_url())
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _("This user is currently assigned to tasks and cannot be deleted"))
            return HttpResponseRedirect(self.get_success_url())
        except IntegrityError:
            messages.error(request, _("Failed to delete user."))
            return HttpResponseRedirect(reverse_lazy('users_list'))
