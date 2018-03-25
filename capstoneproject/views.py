"""
This file contains functions that will correspond with the HTML pages for the web application.
Each HTML page will call a function which will provide the site's functionality.
"""
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf

from capstoneproject.forms import SignUpForm, LoginForm
from capstoneproject.content_rating.algorithm import content_rating


def login(request):
    """
    This function handles HTML requests from the Login page.
    :param request: The HTML request containing the user's action.
    :return: Renders the proper HTML page depending on the user's actions.
    """
    if request.method == 'POST':
        if request.POST.get('submit') == 'signup':  # Check if the user is trying to sign up for a new account.
            form = SignUpForm(request.POST)  # Create a sign up form from the HTML request.
            if form.is_valid():  # Check if the form is valid.
                form.save()
                # Obtain the username and password from the valid form.
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                # Authenticate and login the user.
                user = authenticate(username=username, password=raw_password)
                auth_login(request, user)
                # Go to the home screen if the user is now authenticated and logged in.
                return render(request, 'homepage.html')
            else:  # Go back to the login in page with a new login form if the user failed to sign up for a new account.
                return render(request, 'login.html', {'login_form': LoginForm(), 'signup_form': form})

        if request.POST.get('submit') == 'login':  # Check if the user is trying to log in to an existing account.
            form = LoginForm(request.POST)  # Create a login form from the HTML request.
            if form.is_valid():  # Check if the form is valid.
                # Obtain the username and password from the valid form and authenticate the info.
                login_username = form.cleaned_data.get('login_username')
                raw_password = form.cleaned_data.get('login_password')
                user = authenticate(username=login_username, password=raw_password)
                if user is not None:  # Get if the user is authenticated, check if they are active or disabled.
                    if user.is_active:  # If the user is active, log in and go to the home page.
                        auth_login(request, user)
                        return redirect('homepage')
                    else:  # If the user is disabled, go back to the login page.
                        login_form = LoginForm()
                        login_form.disabled_account_error()
                        return render(request, 'login.html', {'login_form': form, 'signup_form': SignUpForm()})
            # If the form is not valid, return to the login page.
            return render(request, 'login.html', {'login_form': LoginForm(), 'signup_form': SignUpForm()})
    else:
        c = {}
        c.update((csrf(request)))
        c.update(({'login_form': LoginForm(), 'signup_form': SignUpForm()}))
        return render_to_response('login.html', c)


def login_redirect(request):
    """
    Function to handle login redirection.
    :param request: The HTML request to handle.
    :return: A redirection to the login page.
    """
    return redirect('login')


@login_required(login_url='/login/')
def homepage(request):
    """
    Function to handle requests on the home page.
    :param request: The HTML request to handle.
    :return: Renders the home page.
    """
    return render(request, 'homepage.html')


def logout(request):
    """
    Function to handle log out requests.
    :param request: The HTML request to handle.
    :return: Renders the login page after logging the user out.
    """
    logout(request)
    return render(request, 'login.html', {'login_form': LoginForm, 'signup_form': SignUpForm})


@login_required(login_url='/login/')
def profile(request):
    """
    Function to handle requests on the profile page.
    :param request: The HTML request to handle.
    :return: Renders the profile page.
    """
    return render(request, 'profile.html')


@login_required(login_url='/login/')
def search(request):
    """
    Function to handle requests to search for entertainment content from web sources.
    :param request: The HTML request to handle.
    :return: Renders the search page.
    """
    cr = content_rating.ContentRating()
    cr.algorithm('')
    return render(request, 'search.html')


@login_required(login_url='/login/')
def upload(request):
    """
    Function to handle requests to upload files to rate.
    :param request: The HTML request to handle.
    :return: Renders the upload page.
    """
    return render(request, 'upload.html')


@login_required(login_url='/login/')
def copy_in(request):
    """
    Function to handle requests to copy text in to rate.
    :param request: The HTML request to handle.
    :return: Renders the copy-in page.
    """
    return render(request, 'copy-in.html')


def about_algorithm(request):
    """
    Function to handle requests on the about algorithm homepage.
    :param request: The HTML request to handle.
    :return: Renders the about algorithm page.
    """
    return render(request, 'algorithm.html')


def about_page(request):
    """
    Function to handle requests on the about us page.
    :param request: The HTML request to handle.
    :return: Renders the about us algorithm page.
    """
    return render(request, 'about.html')


@login_required(login_url='/login/')
def words(request):
    """
    Function to handle requests on the page containing the offensive words and their levels of offensiveness.
    :param request: The HTML request to handle.
    :return: Renders the words page.
    """
    return render(request, 'words.html')


@login_required(login_url='/login/')
def rating_results(request):
    """
    Function to handle requests on the rating results page.
    :param request: The HTML request to handle.
    :return: Renders the rating results page.
    """
    return render(request, 'rating-result.html')


@login_required(login_url='/login/')
def compare_results(request):
    """
    Function to handle requests to compare rating results.
    :param request: The HTML request to handle.
    :return: Renders the compare page.
    """
    return render(request, 'compare.html')


@login_required(login_url='/login/')
def word_counts(request):
    """
    Function to handle requests to the word counts page.
    :param request: The HTML request to handle.
    :return: Renders the word-counts page.
    """
    return render(request, 'word-counts.html')
