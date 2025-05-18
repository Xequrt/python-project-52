from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse

class UserListView(ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'

class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users_list')

class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users_list')

class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users_list')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('users_list'))
        else:
            # Handle login failure
            pass
    else:
        # Handle GET request, probably render a login form
        pass

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('users_list'))