from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('index')
    success_message = _("You are logged in")

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return response
        except IntegrityError:
            messages.error(self.request,
                           _("Please enter a valid username and password."
                             "Both fields may be case sensitive. "))
            return self.render_to_response(self.get_context_data(form=form))
    #
    def get_success_url(self):
        return reverse_lazy('index')


class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('index')