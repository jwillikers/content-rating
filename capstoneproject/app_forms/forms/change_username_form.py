"""
This file contains a class of a form that changes a user's username.
"""
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class ChangeUsernameForm(forms.ModelForm):
    """
    A form on the Profile page that handles the user changing their username.
    """
    error_messages = {
        'unavailable_username': _("The username is unavailable.")}

    profile_username = forms.CharField(
        label=_("New Username"),
        max_length=20,
        strip=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter username'}),
        help_text=_("Enter a new username with less than 20 characters."))

    class Meta:
        model = User
        fields = ('profile_username', )

    def __init__(self, *args, **kwargs):
        """
        Initialize a change-username form.
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

    def _post_clean(self):
        """
        Clean the change-username form.
        :return: None.
        """
        super()._post_clean()

    def save_username(self, request):
        """
        Updates the user's username to the new value.
        :param request: The HTML request containing the user's current information.
        :return: True if the username was updated.
        """
        user = request.user
        user.username = self.cleaned_data['profile_username']
        user.save()
        return True

    def username_available(self):
        """
        Checks if the desired new username is available. Raises a Validation Error if the username is unavailable.
        :return: None.
        """
        if User.objects.filter(username=self.cleaned_data['profile_username']).exists():
            raise forms.ValidationError(self.error_messages['unavailable_username'], code='unavailable_username')

    def update_username(self, request):
        """
        This function facilitates changing the user's username.
        :param request: The HTML request containing the user's current information.
        :return: False if the username could not be changed, otherwise True.
        """
        try:
            self.username_available()
        except forms.ValidationError as error:
            self.add_error('profile_username', error)
            return False
        return self.save_username(request)
