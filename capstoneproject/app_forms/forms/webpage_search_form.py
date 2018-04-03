"""
This file contains the WebsiteSearchForm that the user fills in when they want to search for a website.
"""
from django import forms
from django.utils.translation import gettext_lazy as _


class WebsiteSearchForm(forms.Form):
    """
        A search song form.
    """
    error_messages = {'website_not_found': _("No website using the given website name was found"),
                      'url_not_found': _("No website using the given URL was found"),
                      'incomplete': _("No website title or URL was provided"),
                      'no_website': _("No website title was provided"),
                      'no_url': _("No url was provided")
                      }

    website_name = forms.CharField(
        label='Name',
        max_length=30,
        strip=False,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter website title'}))

    url = forms.CharField(
        label='URL',
        max_length=40,
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
        website = self.cleaned_data.get('website_name')
        if not url and not website:
            self.add_error('url', self.error_messages['incomplete'])
        elif url is not None and url.strip() == '':
            self.no_url_error()
        elif website is not None and website.strip() == '':
            self.no_website_error()

    def url_not_found(self):
        """
        Add a not found error to the url field.
        :return: None.
        """
        self.add_error('url', self.error_messages['url_not_found'])

    def website_not_found(self):
        """
        Add a not found error to the website name field.
        :return: None.
        """
        self.add_error('website_name', self.error_messages['website_not_found'])

    def no_url_error(self):
        """
        Add a no url error to the url field if no url was given.
        :return: None.
        """
        self.add_error('url', self.error_messages['no_url'])

    def no_website_error(self):
        """
        Add a no website title error to the website name field if no website title was given.
        :return: None.
        """
        self.add_error('website_name', self.error_messages['no_website'])

    def get_website_name(self):
        return self.cleaned_data['website_name']

    def get_url(self):
        return self.cleaned_data['url']
