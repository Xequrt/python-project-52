from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from rollbar.contrib.django.middleware import RollbarNotifierMiddleware


class IndexView(TemplateView, RollbarNotifierMiddleware):
    template_name = 'index.html'

    def get_extra_data(self, request, exc):
        extra_data = dict()

        # Example of adding arbitrary metadata (optional)
        extra_data = {
            'trace_id': 'aabbccddeeff',
            'feature_flags': [
                'feature_1',
                'feature_2',
            ]
        }

        return extra_data

    def get_payload_data(self, request, exc):
        payload_data = dict()

        if not request.user.is_anonymous:
            # Adding info about the user affected by this event (optional)
            # The 'id' field is required, anything else is optional
            payload_data = {
                'person': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                },
            }

        return payload_data

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
        if request.method == 'GET':
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('index')