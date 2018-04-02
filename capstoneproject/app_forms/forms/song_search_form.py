"""
This file contains the SongSearchForm that the user fills in when they want to search for a song.
"""
from django import forms
from django.utils.translation import gettext_lazy as _


class SongSearchForm(forms.Form):
    """
        A search song form.
    """
    error_messages = {'not_found': _("No song using the given title and given artist was found")}

    song_title = forms.CharField(
        label='Song Title',
        max_length=30,
        strip=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter song title'}))

    song_artist = forms.CharField(
        label='Artist',
        max_length=30,
        strip=False,
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

    def not_found(self):
        """
        Add a not found error to the song artist field.
        :return: None.
        """
        self.add_error('song_artist', self.error_messages['not_found'])

    def get_song_title(self):
        return self.cleaned_data['song_title']

    def get_song_artist(self):
        return self.cleaned_data['song_artist']

