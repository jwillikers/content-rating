"""
This file contains the WebsiteSearchForm that the user fills in when they want to search for a website.
"""
from django import forms
from django.utils.translation import gettext_lazy as _


class WebsiteSearchForm(forms.Form):
    """
    A search song form.
    """
    error_messages = {'url_not_found': _("No website using the given URL was found"),
                      'no_url': _("No URL was provided")
                      }

    url = forms.CharField(
        label='URL',
        max_length=50,
        strip=False,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter url'}))

    def __init__(self, *args, **kwargs):
        """
        Initialize the website search form.
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

    def _post_clean(self):
        """
        Clean the website search form.
        :return: None.
        """
        super()._post_clean()
        url = self.cleaned_data.get('url')
        if not url:
            self.no_url_error()
        elif url is not None and url.strip() == '':
            self.no_url_error()

    def url_not_found(self):
        """
        Add a not found error to the url field.
        :return: None.
        """
        self.add_error('url', self.error_messages['url_not_found'])

    def no_url_error(self):
        """
        Add a no url error to the url field if no url was given.
        :return: None.
        """
        self.add_error('url', self.error_messages['no_url'])

    def get_url(self):
        """
        Returns the value from the url field.
        :return: A string, the value from the url field.
        """
        return self.cleaned_data['url']

    def get_title(self):
        """
        Returns the value from either the url field.
        :return: A string, the url.
        """
        if self.cleaned_data.get('url'):
            return self.get_url()
        else:
            return 'webpage'

    def get_creator(self):
        """
        Returns the default value associated with the creator.
        :return: A string, the default value associated with the creator.
        """
        return ''
