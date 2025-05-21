from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomUserForm(UserCreationForm):
    email = forms.EmailField(
        label=_('Email'),
        required=True,
        help_text=_('Required. Enter a valid email address.')
    )
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
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            'username': _('Username'),
            'password1': _('Password'),
            'password2': _('Password confirmation'),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_('Email already exists.'))
        return email

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if not first_name.isalpha():
            self.add_error('first_name', _('First name should contain only letters.'))
        if not last_name.isalpha():
            self.add_error('last_name', _('Last name should contain only letters.'))

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user
