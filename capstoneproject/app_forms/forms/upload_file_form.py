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

    error_messages = {'content_type': _("Files of type %(content_type)s are not supported"),
                      'no_file': _("No file was provided")}
    supported_filetypes = ['docx', 'pdf', 'txt', 'epub']

    file = forms.FileField(
        label='File input',
        help_text="Choose a file you'd like to have rated.",
        required=False,
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
        if self.cleaned_data.get("file") is None:
            self.no_file_error()

    def unknown_filetype_error(self):
        """
        Add an unknown_filetype error to the file field.
        :return: None.
        """
        self.add_error('file', self.error_messages['content_type'], 'content_type')

    def no_file_error(self):
        """
        Add a no file error to the file field if no file was given.
        :return: None.
        """
        self.add_error('file', self.error_messages['no_file'])
