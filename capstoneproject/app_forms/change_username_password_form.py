"""
This file contains a class of a form that changes a user's username and password.
"""
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class ChangeUsernamePasswordForm(forms.ModelForm):
    """
        A form that changes the user's username and password.
    """
    error_messages = {
        'unavailable_username': _("The username is unavailable."),
        'password_mismatch': _("The two password fields didn't match.")}

    profile_username_both = forms.CharField(
        label=_("Username"),
        max_length=20,
        strip=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter username'}),
        help_text=_("Enter a username with less than 20 characters."))

    profile_password_both = forms.CharField(
        label=_("Password"),
        max_length=20,
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter password'}))

    profile_confirm_password_both = forms.CharField(
        label=("Confirm Password"),
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
        fields = ('profile_username_both', 'profile_password_both', 'profile_confirm_password_both')

    def __init__(self, *args, **kwargs):
        """
        Initialize a change-username-and-password form.
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

    def clean_profile_confirm_password_both(self):
        """
        Clean the change-username-and-password form. Raise an error if the passwords do not match,
        otherwise return the password.
        :return: The password provided.
        """
        password1 = self.cleaned_data.get("profile_password_both")
        password2 = self.cleaned_data.get("profile_confirm_password_both")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch')
        return password2

    def _post_clean(self):
        """
        Clean the change-username-and-password form by validating the password is sufficiently difficult.
        :return: None.
        """
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('profile_confirm_password_both')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('profile_confirm_password_both', error)

    def save_profile(self, request):
        """
        This function saves the user's new username and new password.
        :param request: The HTML request containing the user's information.
        :return: True if the information was updated successfully.
        """
        user = request.user
        user.username = self.cleaned_data['profile_username_both']
        user.set_password(self.cleaned_data['profile_confirm_password_both'])
        user.save()
        return True

    def username_available(self):
        """
        This function checks if a username is available or already being used. If the username is not available, a
        Validation Error will be raised.
        :return: None.
        """
        if User.objects.filter(username=self.cleaned_data['profile_username_both']).exists():
            raise forms.ValidationError(self.error_messages['unavailable_username'], code='unavailable_username')

    def update_profile(self, request):
        """
        This function facilitates updating the username and password.
        :param request: The HTML requets containing the user's existing information.
        :return: False if the profile was not updates, otherwise True.
        """
        try:
            self.username_available()
        except forms.ValidationError as error:
            self.add_error('profile_username_both', error)
            return False
        return self.save_profile(request)
