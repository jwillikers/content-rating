from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.utils.translation import gettext, gettext_lazy as _


class LoginForm(forms.ModelForm):
    """
        A login form.
    """
    error_messages = {'invalid_login': _("Invalid username or password."),
                      'disabled_account': _("Account is disabled.")}

    login_username = forms.CharField(
        label='Username',
        max_length=20,
        strip=False,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Enter username'}))
    login_password = forms.CharField(
        label='Password',
        max_length=20,
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Enter password'}))

    class Meta:
        model = User
        fields = ('login_username', 'login_password',)

    def __init__(self, *args, **kwargs):
        """
        Initialize the login form.
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

    def _post_clean(self):
        """
        Clean the login form.
        :return: None.
        """
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('login_password')
        if password:
            try:
                password_validation.validate_password(password, self.instance, password_validators=[])
            except forms.ValidationError as error:
                self.add_error('login_password', error)

    def invalid_login_error(self):
        """
        Raises an invalid login error.
        :return: None.
        """
        self.add_error('login_password', self.error_messages['invalid_login'])

    def disabled_account_error(self):
        """
        Raises an disabled account error.
        :return: None.
        """
        self.add_error('login_username', self.error_messages['disabled_account'])


class SignUpForm(forms.ModelForm):
    """
        A form that creates a user, with no privileges, from the given username and
        password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match.")}

    username = forms.CharField(
        label=_("Username"),
        max_length=20,
        strip=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter username'}),
        help_text=_("Enter a username with less than 20 characters."))

    password1 = forms.CharField(
        label=_("Password"),
        max_length=20,
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter password'}))
    password2 = forms.CharField(
        label=("Password Confirmation"),
        max_length=20,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Confirm password'}),
        strip=False,
        help_text=("Enter the same password as before, for verification."))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """
        Initialize a signup form.
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        """
        Clean the sign up form. Raise an error if the passwords do not match, otherwise return the password.
        :return: The password provided.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch')
        return password2

    def _post_clean(self):
        """
        Clean the sign up form.
        :return: None.
        """
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        """
        Saves a new account if the information is valid.
        :param commit: Saves the user if True.
        :return: The user.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProfileUsernameForm(forms.ModelForm):
    """
    A form on the Profile page that handles the user changing their username.
    """
    error_messages = {
        'unavailable_username': _("The username is unavailable.")}

    profile_username = forms.CharField(
        label=_("New Username"),
        max_length=20,
        strip=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter username'}),
        help_text=_("Enter a new username with less than 20 characters."))

    class Meta:
        model = User
        fields = ('profile_username', )

    def __init__(self, *args, **kwargs):
        """
        Initialize a signup form.
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

    def _post_clean(self):
        """
        Clean the sign up form.
        :return: None.
        """
        super()._post_clean()

    def save_username(self, request):
        user = request.user
        user.username = self.cleaned_data['profile_username']
        user.save()
        return True

    def username_available(self):
        if User.objects.filter(username=self.cleaned_data['profile_username']).exists():
            raise forms.ValidationError(self.error_messages['unavailable_username'], code='unavailable_username')

    def update_username(self, request):
        try:
            self.username_available()
        except forms.ValidationError as error:
            self.add_error('profile_username', error)
            return False
        return self.save_username(request)


class ProfilePasswordForm(forms.ModelForm):
    """
    A form on the Profile page that handles the user changing their password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match.")}

    profile_password = forms.CharField(
        label=_("New Password"),
        max_length=20,
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter password'}))

    profile_confirm_password = forms.CharField(
        label="Confirm Password",
        max_length=20,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Confirm password'}),
        strip=False,
        help_text="Enter the same password as before, for verification.")

    class Meta:
        model = User
        fields = ('profile_password', 'profile_confirm_password')

    def __init__(self, *args, **kwargs):
        """
        Initialize a signup form.
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

    def clean_profile_confirm_password(self):
        """
        Clean the sign up form. Raise an error if the passwords do not match, otherwise return the password.
        :return: The password provided.
        """
        password1 = self.cleaned_data.get("profile_password")
        password2 = self.cleaned_data.get("profile_confirm_password")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch')
        return password2

    def _post_clean(self):
        """
        Clean the sign up form.
        :return: None.
        """
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('profile_confirm_password')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('profile_confirm_password', error)

    def update_password(self, request):
        user = request.user
        user.set_password(self.cleaned_data['profile_confirm_password'])
        user.save()
        return user


class ProfileUsernamePasswordForm(forms.ModelForm):
    """
        A form that changes the user's username and password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match.")}

    profile_username_both = forms.CharField(
        label=_("Username"),
        max_length=20,
        strip=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter username'}),
        help_text=_("Enter a username with less than 20 characters."))

    profile_password_both = forms.CharField(
        label=_("Password"),
        max_length=20,
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter password'}))

    profile_confirm_password_both = forms.CharField(
        label=("Confirm Password"),
        max_length=20,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Confirm password'}),
        strip=False,
        help_text=("Enter the same password as before, for verification."))

    class Meta:
        model = User
        fields = ('profile_username_both', 'profile_password_both', 'profile_confirm_password_both')

    def __init__(self, *args, **kwargs):
        """
        Initialize a signup form.
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

    def clean_profile_confirm_password_both(self):
        """
        Clean the sign up form. Raise an error if the passwords do not match, otherwise return the password.
        :return: The password provided.
        """
        password1 = self.cleaned_data.get("profile_password_both")
        password2 = self.cleaned_data.get("profile_confirm_password_both")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch')
        return password2

    def _post_clean(self):
        """
        Clean the sign up form.
        :return: None.
        """
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('profile_confirm_password_both')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('profile_confirm_password_both', error)

    def save(self, commit=True):
        """
        Saves a new account if the information is valid.
        :param commit: Saves the user if True.
        :return: The user.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["profile_password_both"])
        if commit:
            user.save()
        return user

