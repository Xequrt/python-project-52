from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, _("You are logged in"))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,
                       _('''Please enter a valid username and password. 
                            Both fields may be case sensitive.'''))
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('index')


class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)