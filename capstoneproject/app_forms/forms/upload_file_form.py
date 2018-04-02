"""
This file contains the UploadFileForm that the user uses to upload a file.
"""
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator


class UploadFileForm(forms.Form):
    """
    An upload file form.
    """

    error_messages = {'content_type': _("Files of type %(content_type)s are not supported")}
    supported_filetypes = ['docx', 'pdf', 'txt', 'epub']

    file = forms.FileField(
        label='File input',
        help_text="Choose a file you'd like to have rated.",
        validators=[FileExtensionValidator(allowed_extensions=supported_filetypes)],
        widget=forms.FileInput(attrs={'class': 'form-control-file',
                                      'aria-describedby': "fileHelp"})
    )

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

    def unknown_filetype_error(self):
        """
        Add an unknown_filetype error to the file field.
        :return: None.
        """
        self.add_error('file', self.error_messages['content_type'], 'content_type')
