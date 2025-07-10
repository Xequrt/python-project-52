from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class CustomUserForm(UserCreationForm):
    first_name = forms.CharField(
        label=_('First name'),
        max_length=30,
        required=True,
        help_text=_('Required. Enter your first name.')
    )
    last_name = forms.CharField(
        label=_('Last name'),
        max_length=30,
        required=True,
        help_text=_('Required. Enter your last name.')
    )

    class Meta:
        model = get_user_model()
        fields = ('first_name',
                  'last_name',
                  'username',
                  'password1',
                  'password2')
        labels = {
            'username': _('Username'),
            'password1': _('Password'),
            'password2': _('Password confirmation'),
        }

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if not first_name.isalpha():
            self.add_error('first_name',
                           _('First name should contain only letters.'))
        if not last_name.isalpha():
            self.add_error('last_name',
                           _('Last name should contain only letters.'))

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user
