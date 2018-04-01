"""
This class contains functions to interact between user interactions provided through HTML requests and the forms that
the user is using.
"""
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login


def attempt_signup(form, request):
    """
    This function attempts to save a new user account, and then authenticate the user and log them in.
    :param form: The form the user filled in to sign up.
    :param request: The HTML request containing the request to sign up.
    :return: None
    """
    form.save()
    # Obtain the username and password from the valid form.
    username = form.cleaned_data.get('username')
    raw_password = form.cleaned_data.get('password1')
    # Authenticate and login the user.
    user = authenticate(username=username, password=raw_password)
    auth_login(request, user)


def authenticate_user(form):
    """
    This function attempts to authenticate an existing user and returns an authenticated user upon completion.
    :param form: The form containing the user's username and password.
    :return: An authenticated user.
    """
    login_username = form.cleaned_data.get('login_username')
    raw_password = form.cleaned_data.get('login_password')
    user = authenticate(
        username=login_username,
        password=raw_password)
    return user
