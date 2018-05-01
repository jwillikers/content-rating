"""
This file contains functions that will correspond with the HTML pages for the
web application. Each HTML page will call a function which will provide the
site's functionality.
"""
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.contrib.auth import views as auth_views
from django.urls import reverse

from capstoneproject.helpers import form_helper, parsing, file_helper
from capstoneproject.helpers.view_helpers import profile_view_helper, ratings_view_helper, view_helper, \
    word_counts_view_helper, words_view_helper
import capstoneproject.app_forms as forms


def login(request):
    """
    This function handles HTML requests from the Login page.
    :param request: The HTML request containing the user's action.
    :return: Renders the proper HTML page depending on the user's actions.
    """
    context = {'login_form': forms.LoginForm(),
               'signup_form': forms.SignUpForm()}

    if request.method == 'POST':
        if request.POST.get('submit') == 'signup':
            form = forms.SignUpForm(request.POST)
            if form.is_valid():  # Check if the form is valid.
                form_helper.signup(form, request)
                # Go to the home screen if the user is now authenticated and
                # logged in.
                return render(request, 'homepage.html')
            else:  # Go back to the login in page with a new login form if the
                context['signup_form'] = form
                return render(request, 'login.html', context)

        if request.POST.get('submit') == 'login':
            form = forms.LoginForm(request.POST)
            if form.is_valid():  # Check if the form is valid.
                user = form_helper.authenticate_user(form)
                if user is not None:
                    if user.is_active:  # Check if user account is active.
                        auth_login(request, user)
                        return redirect('homepage')
                    else:  # User account is disabled.
                        context['login_form'].disabled_account_error()
                        return render(request, 'login.html', context)
                else:
                    form.invalid_login_error()
            # If the form is not valid, return to the login page.
            context['login_form'] = form
            return render(request, 'login.html', context)
    else:
        c = {}
        c.update((csrf(request)))
        c.update(({'login_form': forms.LoginForm(), 'signup_form': forms.SignUpForm()}))
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
    if request.session.get('delete'):
        del request.session['delete']
        if request.session.get('content_compare'):
            del request.session['content_compare']
    if request.method == "POST":
        request.session['content_compare'] = request.POST['content_compare']
    return render(request, 'homepage.html')


def logout(request):
    """
    Function to handle log out requests.
    :param request: The HTML request to handle.
    :return: Renders the login page after logging the user out.
    """
    auth_views.logout(request=request, next_page='login/')
    return render(request, 'login.html',
                  {'login_form': forms.LoginForm(), 'signup_form': forms.SignUpForm()})


@login_required(login_url='/login/')
def profile(request):
    """
    Function to handle requests on the profile page.
    :param request: The HTML request to handle.
    :return: Renders the profile page.
    """
    if request.session.get('delete'):
        del request.session['delete']
        if request.session.get('content_compare'):
            del request.session['content_compare']

    context = profile_view_helper.get_profile_context(request.user)
    if request.method == 'POST':
        if request.POST.get('submit_username') == 'username':
            form = forms.ChangeUsernameForm(request.POST)
            if form.is_valid():  # Check if the form is valid.
                if form.update_username(request):  # Update the username and return to profile page
                    return render(request, 'profile.html', context)
                else:  # Return to profile page and display errors
                    context['change_username_form'] = form
                    return render(request, 'profile.html', context)
            else:  # Go back to the profile page and display errors
                context['change_username_form'] = form
                return render(request, 'profile.html', context)

        elif request.POST.get('submit_password') == 'password':
            form = forms.ChangePasswordForm(request.POST)
            if form.is_valid():  # Check if the form is valid.
                form.update_password(request)  # Update the user's password and return to profile page
                return render(request, 'profile.html', context)
            else:  # Go back to the profile page and display errors
                context['change_password_form'] = form
                return render(request, 'profile.html', context)

        elif request.POST.get('submit_both') == 'both':
            form = forms.ChangeUsernamePasswordForm(request.POST)
            if form.is_valid():  # Check if the form is valid.
                form.update_profile(request)  # Update the username and password and return to profile page
                return render(request, 'profile.html', context)
            else:  # Go back to the profile page and display errors
                context['change_username_password_form'] = form
                return render(request, 'profile.html', context)

        elif request.POST.get('submit_category_weights') == 'category_weights':
            profile_view_helper.update_user_category_weights(request)

    return render(request, 'profile.html', context)


@login_required(login_url='/login/')
def search(request):
    """
    Function to handle requests to search for entertainment content from web
        sources.
    :param request: The HTML request to handle.
    :return: Renders the search page.
    """
    context = {'song_search_form': forms.SongSearchForm(),
               'website_search_form': forms.WebsiteSearchForm()}

    if request.session.get('delete'):
        del request.session['delete']
        if request.session.get('content_compare'):
            del request.session['content_compare']

    if request.method == 'GET':
        if request.session.get('invalid_song'):  # Check if the user submitted an invalid search of a song.
            del request.session['invalid_song']
            form = forms.SongSearchForm(request.GET)
            form.is_valid()
            context['song_search_form'] = form
        elif request.session.get('song_not_found'):  # Check if the previous song search was not found.
            del request.session['song_not_found']
            if request.session.get('song_title'):  # Fill in the song title field with the user's past request
                title = request.session.get('song_title')
                del request.session['song_title']
            else:
                title = ''
            if request.session.get('song_artist'):  # Fill in the song artist field with the user's past request
                artist = request.session.get('song_artist')
                del request.session['song_artist']
            else:
                artist = ''
            form = forms.SongSearchForm(request.GET,
                                        initial={'song_title': str(title),
                                                 'song_artist': str(artist)})
            form.not_found = True
            form.is_valid()
            form.not_found_error()  # Error since the song-artist combo did not match a song
            context['song_search_form'] = form
        elif request.session.get('invalid_website'):  # Check if the user submitted an invalid search of a website
            del request.session['invalid_website']
            form = forms.WebsiteSearchForm(request.GET)
            form.is_valid()
            context['website_search_form'] = form

    return render(request, 'search.html', context)


@login_required(login_url='/login/')
def upload(request):
    """
    Function to handle requests to upload files to rate.
    :param request: The HTML request to handle.
    :return: Renders the upload page.
    """
    context = {'upload_file_form': forms.UploadFileForm()}

    if request.session.get('delete'):
        del request.session['delete']
        if request.session.get('content_compare'):
            del request.session['content_compare']

    if request.method == 'GET':
        if request.session.get('invalid_file'):  # Check if the last provided file was invalid.
            del request.session['invalid_file']
            form = forms.UploadFileForm(request.GET)
            form.is_valid()
            context['upload_file_form'] = form

    return render(request, 'upload.html', context)


@login_required(login_url='/login/')
def copy_in(request):
    """
    Function to handle requests to copy text in to rate.
    :param request: The HTML request to handle.
    :return: Renders the copy-in page.
    """
    context = {'copy_in_form': forms.CopyInForm()}
    if request.session.get('delete'):
        del request.session['delete']
        if request.session.get('content_compare'):
            del request.session['content_compare']

    if request.method == 'GET':
        if request.session.get('invalid_content'):  # Check if the last copy-in text provided was invalid.
            del request.session['invalid_content']
            form = forms.CopyInForm(request.GET)
            form.is_valid()
            context['copy_in_form'] = form

    return render(request, 'copy-in.html', context)


def about_algorithm(request):
    """
    Function to handle requests on the about algorithm homepage.
    :param request: The HTML request to handle.
    :return: Renders the about algorithm page.
    """
    if request.session.get('delete'):
        del request.session['delete']
        if request.session.get('content_compare'):
            del request.session['content_compare']
    return render(request, 'algorithm.html')


def about_page(request):
    """
    Function to handle requests on the about us page.
    :param request: The HTML request to handle.
    :return: Renders the about us algorithm page.
    """
    if request.session.get('delete'):
        del request.session['delete']
        if request.session.get('content_compare'):
            del request.session['content_compare']
    return render(request, 'about.html')


@login_required(login_url='/login/')
def words(request, category):
    """
    Function to handle requests on the page containing the offensive words and
        their levels of offensiveness.
    :param request: The HTML request to handle.
    :param category: The category to display.
    :return: Renders the words page.
    """
    if request.session.get('delete'):
        del request.session['delete']
        if request.session.get('content_compare'):
            del request.session['content_compare']

    if request.method == 'POST':
        if request.POST.get('submit_word_weights') == 'word_weights':
            words_view_helper.update_user_word_weights(request, category)
            return HttpResponseRedirect(reverse('profile'))

    context = words_view_helper.get_words_context(request.user, category)

    return render(request, 'words.html', context)


@login_required(login_url='/login/')
def rating_results(request):
    """
    Function to handle requests on the rating results page.
    :param request: The HTML request to handle.
    :return: Renders the rating results page.
    """
    context = dict()  # initialize default context

    if request.method == 'POST':
        if request.POST.get('submit') == 'copy-in':  # Copy in request
            form = forms.CopyInForm(request.POST)
            if form.is_valid():  # Check if the form is valid.
                # Rate text here
                text_str = form.get_text()  # Get text
                context = ratings_view_helper.perform_rating(text_str, form, request)  # Rate content and get results
            else:
                request.session['invalid_content'] = True
                return HttpResponseRedirect(reverse('copy'))
        elif request.POST.get('submit') == 'song':  # Song request
            form = forms.SongSearchForm(request.POST)
            if form.is_valid():  # Check if the form is valid.
                title = form.get_title()  # Get title
                artist = form.get_creator()  # Get artist
                text_str = parsing.search_songs(title, artist)  # Get text

                if text_str == 0:  # No song matched the song title and artist, return to Search page
                    request.session['song_not_found'] = True
                    request.session['song_artist'] = artist
                    request.session['song_title'] = title
                    return HttpResponseRedirect(reverse('search'))

                context = ratings_view_helper.perform_rating(text_str, form, request)  # Rate content and get results
            else:
                request.session['invalid_song'] = True
                return HttpResponseRedirect(reverse('search'))
        elif request.POST.get('submit') == 'webpage':  # Webpage request
            form = forms.WebsiteSearchForm(request.POST)
            if form.is_valid():
                # Find if user wanted to search url or website title
                url = form.get_url()
                text_str = ''
                if url:  # Get text from url
                    text_str = parsing.search_website(url)
                context = ratings_view_helper.perform_rating(text_str, form, request)  # Rate content and get results
            else:
                request.session['invalid_website'] = True
                return HttpResponseRedirect(reverse('search'))
        elif request.POST.get('submit') == 'file':  # File request
            form = forms.UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                text_str = file_helper.get_file_content(request.FILES['file'])  # Get text from file
                context = ratings_view_helper.perform_rating(text_str, form, request)  # Rate content and get results
            else:
                request.session['invalid_file'] = True
                return HttpResponseRedirect(reverse('upload'))
    # print(context)
    if request.session.get('content_compare'):  # Go to compare screen if the user last clicked Compare
        return redirect('compare')
    return render(request, 'rating-result.html', context)


@login_required(login_url='/login/')
def compare_results(request):
    """
    Function to handle requests to compare rating results.
    :param request: The HTML request to handle.
    :return: Renders the compare page.
    """
    context = dict()

    if request.session.get('content_compare'):
        content_compare = request.session['content_compare']  # name of item to be compared.
        del request.session['content_compare']

        previous_rating = ratings_view_helper.get_rating(request.user, 1)  # Get the older rating.
        if previous_rating:
            previous_context = ratings_view_helper.get_rating_results_context(previous_rating, 'previous')
            context.update(previous_context)

        current_rating = ratings_view_helper.get_rating(request.user, 0)  # Get the newer rating.
        if current_rating:
            current_context = ratings_view_helper.get_rating_results_context(current_rating, 'current')
            context.update(current_context)

    request.session['delete'] = True

    return render(request, 'compare.html', context)


@login_required(login_url='/login/')
def word_counts(request, name):
    """
    Function to handle requests to the word counts page.
    :param request: The HTML request to handle.
    :param name: a String, the name of the value of which to display the words counts.
    :return: Renders the word-counts page.
    """

    if name == 'current':
        context = word_counts_view_helper.get_word_counts_context(request.user, 0)  # Get the newer rating.
    elif name == 'previous':
        context = word_counts_view_helper.get_word_counts_context(request.user, 1)  # Get the older rating from comparison.
    else:
        context = dict()
    return render(request, 'word-counts.html', context)
