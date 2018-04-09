"""
This file contains a class of a form that signs up a new user.
"""
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class SignUpForm(forms.ModelForm):
    """
        A form that creates a user, with no privileges, from the given username and
        password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match.")}

    username = forms.CharField(
        label=_("Username"),
        max_length=20,
        strip=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter username'}),
        help_text=_("Enter a username with less than 20 characters."))

    password1 = forms.CharField(
        label=_("Password"),
        max_length=20,
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter password'}))

    password2 = forms.CharField(
        label=("Password Confirmation"),
        max_length=20,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Confirm password'}),
        strip=False,
        help_text=("Enter the same password as before, for verification."))

    class Meta:
        """
        Passes additional data to the Meta class.
        """
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """
        Initialize a signup form.
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        """
        Clean the sign up form. Raise an error if the passwords do not match, otherwise return the password.
        :return: The password provided.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch')
        return password2

    def _post_clean(self):
        """
        Clean the sign up form.
        :return: None.
        """
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
        """
        Saves a new account if the information is valid.
        :param commit: Saves the user if True.
        :return: The user.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
