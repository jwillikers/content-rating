# import unicodedata

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _


class LoginForm(forms.ModelForm):
    """
        A login form.
    """
    error_messages = {
        'invalid_login': _("Invalid username or password."),
        'disabled_account': _("Account is disabled."),
    }

    login_username = forms.CharField(label='Username',
                               max_length=20,
                               strip=False,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Enter username'}))

    login_password = forms.CharField(label='Password',
                               max_length=20,
                               strip=False,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Enter password'}))

    class Meta:
        model = User
        fields = ('login_username', 'login_password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('login_password')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('login_password', error)

    def invalid_login_error(self):
        raise forms.ValidationError(
            self.error_messages['invalid_login'],
#            code='invalid_login',
        )

    def disabled_account_error(self):
        raise forms.ValidationError(
            self.error_messages['disabled_account'],
#            code='disabled_account',
        )


class SignUpForm(forms.ModelForm):
    """
        A form that creates a user, with no privileges, from the given username and
        password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    username = forms.CharField(
        label=_("Username"),
        max_length=20,
        strip=False,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter username'}),
        help_text=_("Enter a username with less than 20 characters."),
    )

    password1 = forms.CharField(
        label=_("Password"),
        max_length=20,
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter password'}),
#        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password Confirmation"),
        max_length=20,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
#        if self._meta.model.USERNAME_FIELD in self.fields:
#            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user