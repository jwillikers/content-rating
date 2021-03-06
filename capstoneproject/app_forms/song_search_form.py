"""
This file contains the SongSearchForm that the user fills in when they want to search for a song.
"""
from django import forms
from django.utils.translation import gettext_lazy as _


class SongSearchForm(forms.Form):
    """
    A search song form.
    """
    not_found = False
    error_messages = {'not_found': _("No song using the given title and given artist was found"),
                      'no_title': _("No song title was provided")}

    song_title = forms.CharField(
        label='Song Title',
        max_length=30,
        strip=False,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter song title'}))

    song_artist = forms.CharField(
        label='Artist',
        max_length=30,
        strip=False,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter artist'}))

    def __init__(self, *args, **kwargs):
        """
        Initialize the song search form.
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

    def _post_clean(self):
        """
        Clean the song search form.
        :return: None.
        """
        super()._post_clean()
        if self.cleaned_data.get("song_title") is not None \
                and self.cleaned_data.get("song_title").strip() == '' \
                and not self.not_found:
            self.no_title_error()

    def not_found_error(self):
        """
        Add a not found error to the song artist field.
        :return: None.
        """
        self.add_error('song_artist', self.error_messages['not_found'])
        self.not_found = False

    def no_title_error(self):
        """
        Add a no title error to the song title field if no song title was given.
        :return: None.
        """
        self.add_error('song_title', self.error_messages['no_title'])

    def get_title(self):
        """
        Returns the song title.
        :return: A string, the song title.
        """
        return self.cleaned_data['song_title'].title()

    def get_creator(self):
        """
        Returns the song artist.
        :return: A string, the song artist.
        """
        return self.cleaned_data['song_artist'].title()

