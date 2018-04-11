"""
This file contains a class of a form that logs an existing user in.
"""
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from capstoneproject.helpers import model_helper





class WordsForm(forms.Form):
    """
    A login form.
    """
    error_messages = {'invalid_login': _("Invalid username or password."),
                      'disabled_account': _("Account is disabled.")}

    def __init__(self, category, *args, **kwargs):
        """
        Initialize the login form.
        :param args:
        :param kwargs:
        """
        super(WordsForm, self).__init__(*args, **kwargs)

        weight_dict = dict()
        for weight in model_helper.get_weights():
            weight_dict[weight[0]] = weight[1]
        weight_levels = len(weight_dict) - 1

        cat_words = model_helper.get_category_words(category)
        for count, word in enumerate(cat_words):
            form_title = '{} {}'.format(count, word)
            self.fields[form_title] = forms.IntegerField(
                label=word,
                strip=False,
                widget=forms.NumberInput(attrs={'type': 'range', 'step': '1', 'min': '0', 'max': str(weight_levels)})
            )


    def _post_clean(self):
        """
        Clean the login form.
        :return: None.
        """
        super()._post_clean()


    def invalid_login_error(self):
        """
        Raises an invalid login error.
        :return: None.
        """
        self.add_error('login_password', self.error_messages['invalid_login'])

