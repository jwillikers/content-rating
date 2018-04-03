"""
This file contains the MovieSearchForm that the user fills in when they want to search for a movie.
"""
from django import forms
from django.utils.translation import gettext_lazy as _


class MovieSearchForm(forms.Form):
    """
        A search movie form.
    """
    error_messages = {'not_found': _("No movie with the given movie title was found"),
                      'no_title': _("No movie title was provided")}

    movie_title = forms.CharField(
        label='Movie Title',
        max_length=30,
        strip=False,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter movie title'}))

    def __init__(self, *args, **kwargs):
        """
        Initialize the movie search form.
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

    def _post_clean(self):
        """
        Clean the movie search form.
        :return: None.
        """
        super()._post_clean()
        if self.cleaned_data.get("movie_title") is not None and self.cleaned_data.get("movie_title").strip() == '':
            self.no_title_error()

    def not_found_error(self):
        """
        Adds an not found error to the movie title field.
        :return: None.
        """
        self.add_error('movie_title', self.error_messages['not_found'])

    def no_title_error(self):
        """
        Add a no title error to the movie title field if no movie title was given.
        :return: None.
        """
        self.add_error('movie_title', self.error_messages['no_title'])

    def get_movie_title(self):
        return self.cleaned_data['movie_title']
