"""
This file contains the CopyInForm that the user fills in when they want to copy in text to rate.
"""
from django import forms
from django.utils.translation import gettext_lazy as _


class CopyInForm(forms.Form):
    """
        A form for the user to copy in text to rate.
    """
    error_messages = {'empty_text': _("No text was provided")}

    copy_in_text = forms.CharField(
        label='Content',
        strip=False,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter text here', 'rows': 10}))

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
        if self.cleaned_data.get("copy_in_text") is not None and self.cleaned_data.get("copy_in_text").strip() == '':
            self.empty_text_error()

    def empty_text_error(self):
        """
        Adds an not found error to the movie title field.
        :return: None.
        """
        self.add_error('copy_in_text', self.error_messages['empty_text'])

    def get_text(self):
        """
        Provides the text in the form's text area where the user provided text.
        :return: A string containing the text from the user.
        """
        return self.cleaned_data['copy_in_text']

    def get_title(self):
        return 'Provided Text'

    def get_creator(self):
        return ''
