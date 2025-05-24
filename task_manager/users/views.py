from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from .forms import CustomUserForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.http import request


class UserListView(ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return super().get_queryset().order_by('username')


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = CustomUserForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('login')
    success_message = "User created successfully!"

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return response
        except IntegrityError:
            messages.error(self.request, "User with this username already exists.")
            return self.render_to_response(self.get_context_data(form=form))


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('users_list')
    success_message = "User updated successfully!"
    login_url = _url = reverse_lazy('login')

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, pk=self.kwargs.get('pk'))

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if not request.user.is_superuser and obj != request.user:
            messages.error(request, "You do not have permission to modify another user.")
            return redirect('users_list')

        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users_list')
    success_message = "User deleted successfully!"
    login_url = _url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.kwargs.get('pk'))

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if not request.user.is_superuser and obj != request.user:
            messages.error(request, "You can only delete your own account.")
            return redirect('users_list')

        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except IntegrityError:
            messages.error(request, "Failed to delete user.")
            return HttpResponseRedirect(reverse_lazy('users_list'))
