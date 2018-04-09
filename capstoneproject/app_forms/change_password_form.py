"""
This file contains a class of a form that changes a user's password.
"""
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class ChangePasswordForm(forms.ModelForm):
    """
    A form on the Profile page that handles the user changing their password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match.")}

    profile_password = forms.CharField(
        label=_("New Password"),
        max_length=20,
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter password'}))

    profile_confirm_password = forms.CharField(
        label="Confirm Password",
        max_length=20,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Confirm password'}),
        strip=False,
        help_text="Enter the same password as before, for verification.")

    class Meta:
        """
        Passes additional data to the Meta class.
        """
        model = User
        fields = ('profile_password', 'profile_confirm_password')

    def __init__(self, *args, **kwargs):
        """
        Initialize a change-password form.
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

    def clean_profile_confirm_password(self):
        """
        Clean the change-password form. Raise an error if the passwords do not match, otherwise return the password.
        :return: The password provided.
        """
        password1 = self.cleaned_data.get("profile_password")
        password2 = self.cleaned_data.get("profile_confirm_password")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch')
        return password2

    def _post_clean(self):
        """
        Clean the change-password form.
        :return: None.
        """
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('profile_confirm_password')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('profile_confirm_password', error)

    def update_password(self, request):
        """
        Updates the user's password.
        :param request: The HTML request containing the user's current information.
        :return: The updated user.
        """
        user = request.user
        user.set_password(self.cleaned_data['profile_confirm_password'])
        user.save()
        return user
