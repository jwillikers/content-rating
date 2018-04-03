"""
This file contains the TVShowSearchForm that the user fills in when they want to search for a TV Show.
"""
from django import forms
from django.utils.translation import gettext_lazy as _


class TVShowSearchForm(forms.Form):
    """
        A search TV show form.
    """
    error_messages = {'not_found': _("No TV Show with the given show title and episode title was found"),
                      'no_show_title': _("No show title was provided"),
                      'no_episode_title': _("No episode title was provided")}

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
        if self.cleaned_data.get("show_title") is not None and self.cleaned_data.get("show_title").strip() == '':
            self.empty_show_title_error()
        if self.cleaned_data.get("episode_title") is not None and self.cleaned_data.get("episode_title").strip() == '':
            self.empty_episode_title_error()

    def not_found_error(self):
        """
        Adds a not found error to the episode title field.
        :return: None.
        """
        self.add_error('episode_title', self.error_messages['not_found'])

    def empty_show_title_error(self):
        """
        Adds an not found error to the show title field.
        :return: None.
        """
        self.add_error('show_title', self.error_messages['no_show_title'])

    def empty_episode_title_error(self):
        """
        Adds an not found error to the episode title field.
        :return: None.
        """
        self.add_error('episode_title', self.error_messages['no_episode_title'])

    def get_episode_title(self):
        return self.cleaned_data['episode_title']

    def get_show_title(self):
        return self.cleaned_data['show_title']
