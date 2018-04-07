"""
This file contains a class of a form that logs an existing user in.
"""
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.ModelForm):
    """
    A login form.
    """
    error_messages = {'invalid_login': _("Invalid username or password."),
                      'disabled_account': _("Account is disabled.")}

    login_username = forms.CharField(
        label='Username',
        max_length=20,
        strip=False,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Enter username'}))
    login_password = forms.CharField(
        label='Password',
        max_length=20,
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Enter password'}))

    class Meta:
        model = User
        fields = ('login_username', 'login_password',)

    def __init__(self, *args, **kwargs):
        """
        Initialize the login form.
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

    def _post_clean(self):
        """
        Clean the login form.
        :return: None.
        """
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('login_password')
        if password:
            try:
                password_validation.validate_password(password, self.instance, password_validators=[])
            except forms.ValidationError as error:
                self.add_error('login_password', error)

    def invalid_login_error(self):
        """
        Raises an invalid login error.
        :return: None.
        """
        self.add_error('login_password', self.error_messages['invalid_login'])

    def disabled_account_error(self):
        """
        Raises an disabled account error.
        :return: None.
        """
        self.add_error('login_username', self.error_messages['disabled_account'])
