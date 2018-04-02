"""
This file contains the TVShowSearchForm that the user fills in when they want to search for a TV Show.
"""
from django import forms
from django.utils.translation import gettext_lazy as _


class TVShowSearchForm(forms.Form):
    """
        A search TV show form.
    """
    error_messages = {'not_found': _("No TV Show with the given show title and episode title was found")}

    show_title = forms.CharField(
        label='Show Title',
        max_length=30,
        strip=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter show title'}))

    episode_title = forms.CharField(
        label='Episode Title',
        max_length=30,
        strip=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter episode title'}))

    def __init__(self, *args, **kwargs):
        """
        Initialize the tv show search form.
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

    def _post_clean(self):
        """
        Clean the tv show search form.
        :return: None.
        """
        super()._post_clean()

    def not_found_error(self):
        """
        Adds a not found error to the episode title field.
        :return: None.
        """
        self.add_error('episode_title', self.error_messages['not_found'])

    def get_episode_title(self):
        return self.cleaned_data['episode_title']

    def get_show_title(self):
        return self.cleaned_data['show_title']
