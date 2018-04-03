"""
This file contains functions that will correspond with the HTML pages for the
web application. Each HTML page will call a function which will provide the
site's functionality.
"""
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.context_processors import csrf
from django.contrib.auth import views as auth_views
from django.urls import reverse

from capstoneproject.display import display_categories, display_words, display_category_words
from capstoneproject.content_rating.algorithm import content_rating
from capstoneproject.models import Weight
from capstoneproject.app_forms import form_handler
from capstoneproject.app_forms.forms.login_form import LoginForm
from capstoneproject.app_forms.forms.signup_form import SignUpForm
from capstoneproject.app_forms.forms.change_password_form import ChangePasswordForm
from capstoneproject.app_forms.forms.change_username_form import ChangeUsernameForm
from capstoneproject.app_forms.forms.change_username_password_form import ChangeUsernamePasswordForm
from capstoneproject.app_forms.forms.song_search_form import SongSearchForm
from capstoneproject.app_forms.forms.tv_show_search_form import TVShowSearchForm
from capstoneproject.app_forms.forms.movie_search_form import MovieSearchForm
from capstoneproject.app_forms.forms.webpage_search_form import WebsiteSearchForm
from capstoneproject.app_forms.forms.copy_in_form import CopyInForm
from capstoneproject.app_forms.forms.upload_file_form import UploadFileForm
from capstoneproject import parsing
from capstoneproject.shared import rater
import os


def login(request):
    """
    This function handles HTML requests from the Login page.
    :param request: The HTML request containing the user's action.
    :return: Renders the proper HTML page depending on the user's actions.
    """
    context = {'login_form': LoginForm(),
               'signup_form': SignUpForm()}

    if request.method == 'POST':
        if request.POST.get('submit') == 'signup':
            form = SignUpForm(request.POST)
            if form.is_valid():  # Check if the form is valid.
                form_handler.signup(form, request)
                # Go to the home screen if the user is now authenticated and
                # logged in.
                return render(request, 'homepage.html')
            else:  # Go back to the login in page with a new login form if the
                context['signup_form'] = form
                return render(request, 'login.html', context)

        if request.POST.get('submit') == 'login':
            form = LoginForm(request.POST)
            if form.is_valid():  # Check if the form is valid.
                user = form_handler.authenticate_user(form)
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
    if request.session.get('delete'):
        del request.session['delete']
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
                  {'login_form': LoginForm(), 'signup_form': SignUpForm()})


@login_required(login_url='/login/')
def profile(request):
    """
    Function to handle requests on the profile page.
    :param request: The HTML request to handle.
    :return: Renders the profile page.
    """
    if request.session.get('delete'):
        del request.session['delete']
        del request.session['content_compare']
    weight_dict = dict()
    for weight in Weight.WEIGHTS:
        weight_dict[weight[0]] = weight[1]
    recently_rated = {'Pillow Talkin': 9,
                      'Baby Got Back': 7,
                      'Africa': 1,
                      'Freebird': 5,
                      'My First Song': 3
                      }

    context = {'categories': display_categories(),
               'recently_rated': recently_rated,
               'weight_levels': len(weight_dict) - 1,
               'weight_dict': weight_dict,
               'change_username_form': ChangeUsernameForm(),
               'change_password_form': ChangePasswordForm(),
               'change_username_password_form': ChangeUsernamePasswordForm()}

    if request.method == 'POST':
        if request.POST.get('submit_username') == 'username':
            form = ChangeUsernameForm(request.POST)
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
            form = ChangePasswordForm(request.POST)
            if form.is_valid():  # Check if the form is valid.
                form.update_password(request)  # Update the user's password and return to profile page
                return render(request, 'profile.html', context)
            else:  # Go back to the profile page and display errors
                context['change_password_form'] = form
                return render(request, 'profile.html', context)

        elif request.POST.get('submit_both') == 'both':
            form = ChangeUsernamePasswordForm(request.POST)
            if form.is_valid():  # Check if the form is valid.
                form.update_profile(request)  # Update the username and password and return to profile page
                return render(request, 'profile.html', context)
            else:  # Go back to the profile page and display errors
                context['change_username_password_form'] = form
                return render(request, 'profile.html', context)

    return render(request, 'profile.html', context)


@login_required(login_url='/login/')
def search(request):
    """
    Function to handle requests to search for entertainment content from web
        sources.
    :param request: The HTML request to handle.
    :return: Renders the search page.
    """
    context = {'song_search_form': SongSearchForm(),
               'tv_search_form': TVShowSearchForm(),
               'movie_search_form': MovieSearchForm(),
               'website_search_form': WebsiteSearchForm()}

    if request.session.get('delete'):
        del request.session['delete']
        del request.session['content_compare']

    if request.method == 'GET':
        if request.session.get('invalid_song'):
            del request.session['invalid_song']
            form = SongSearchForm(request.GET)
            form.is_valid()
            context['song_search_form'] = form
        elif request.session.get('invalid_tv_show'):
            del request.session['invalid_tv_show']
            form = TVShowSearchForm(request.GET)
            form.is_valid()
            context['tv_search_form'] = form
        elif request.session.get('invalid_movie'):
            del request.session['invalid_movie']
            form = MovieSearchForm(request.GET)
            form.is_valid()
            context['movie_search_form'] = form
        elif request.session.get('invalid_website'):
            del request.session['invalid_website']
            form = WebsiteSearchForm(request.GET)
            form.is_valid()
            context['website_search_form'] = form

    if request.method == 'POST':
        if request.POST.get('submit') == 'song':  # Song request
            form = SongSearchForm(request.POST)
            if form.is_valid():  # Check if the form is valid.
                return redirect('results')  # Go to the rating results page if valid.
            else:
                context['song_search_form'] = form  # Display errors if invalid.
        elif request.POST.get('submit') == 'tv_show':  # TV show request
            form = TVShowSearchForm(request.POST)
            if form.is_valid():
                return redirect('results')  # Go to the rating results page if valid.
            else:
                context['tv_search_form'] = form  # Display errors if invalid.
        elif request.POST.get('submit') == 'movie':  # Movie request
            form = MovieSearchForm(request.POST)
            if form.is_valid():
                return redirect('results')  # Go to the rating results page if valid.
            else:
                context['movie_search_form'] = form  # Display errors if invalid.
        elif request.POST.get('submit') == 'webpage':  # Website request
            form = WebsiteSearchForm(request.POST)
            if form.is_valid():
                return redirect('results')  # Go to the rating results page if valid.
            else:
                context['website_search_form'] = form  # Display errors if invalid.
    # rater.algorithm('')
    return render(request, 'search.html', context)


@login_required(login_url='/login/')
def upload(request):
    """
    Function to handle requests to upload files to rate.
    :param request: The HTML request to handle.
    :return: Renders the upload page.
    """
    context = {'upload_file_form': UploadFileForm()}

    if request.session.get('delete'):
        del request.session['delete']
        del request.session['content_compare']

    if request.method == 'POST':
        if request.POST.get('submit') == 'file':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():  # Check if the form is valid.
                return rating_results(request)  # If the form is valid, go to the results page.
            else:
                context['upload_file_form'] = form  # Form is invalid, keep the same form to provide error messages.

    return render(request, 'upload.html', context)


@login_required(login_url='/login/')
def copy_in(request):
    """
    Function to handle requests to copy text in to rate.
    :param request: The HTML request to handle.
    :return: Renders the copy-in page.
    """
    context = {'copy_in_form': CopyInForm()}
    if request.session.get('delete'):
        del request.session['delete']
        del request.session['content_compare']

    if request.method == 'GET':
        if request.session.get('invalid_content'):
            del request.session['invalid_content']
            form = CopyInForm(request.GET)
            form.is_valid()
            context['copy_in_form'] = form

    if request.method == 'POST':
        if request.POST.get('submit') == 'copy-in':
            form = CopyInForm(request.POST)
            if form.is_valid():  # Check if the form is valid.
                return rating_results(request)  # If the form is valid, go to the results page.
            else:
                context['copy_in_form'] = form  # Form is invalid, keep the same form to provide error messages.

    return render(request, 'copy-in.html', context)


def about_algorithm(request):
    """
    Function to handle requests on the about algorithm homepage.
    :param request: The HTML request to handle.
    :return: Renders the about algorithm page.
    """
    if request.session.get('delete'):
        del request.session['delete']
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
        del request.session['content_compare']
    return render(request, 'about.html')


@login_required(login_url='/login/')
def words(request, category):
    """
    Function to handle requests on the page containing the offensive words and
        their levels of offensiveness.
    :param request: The HTML request to handle.
    :return: Renders the words page.
    """
    if request.session.get('delete'):
        del request.session['delete']
        del request.session['content_compare']
    weight_dict = dict()
    for weight in Weight.WEIGHTS:
        weight_dict[weight[0]] = weight[1]
    context = {'category': category,
               'words': display_category_words(category),
               'weight_levels': len(weight_dict) - 1,
               'weight_dict': weight_dict
               }
    return render(request, 'words.html', context)


@login_required(login_url='/login/')
def rating_results(request):
    """
    Function to handle requests on the rating results page.
    :param request: The HTML request to handle.
    :return: Renders the rating results page.
    """
    if 'content_compare' in request.session:
        return redirect('compare')
    category_ratings = dict()
    category_word_counts = dict()
    for category in display_categories():
        category_ratings[category.name] = 5
        category_word_counts[category.name] = {'word1': 4,
                                               'word2': 3,
                                               'word3': 2
                                               }
    context = {'name': 'Pillow Talkin',
               'creator': "Lil' Dicky (feat. BRAIN)",
               'overall_rating': 7,
               'category_ratings': category_ratings,
               'category_word_counts': category_word_counts
               }

    if request.method == 'POST':
        if request.POST.get('submit') == 'copy-in':
            form = CopyInForm(request.POST)
            if form.is_valid():  # Check if the form is valid.
                # Rate text here
                text = form.cleaned_data.get('copy_in_text')
                print(text)
            else:
                request.session['invalid_content'] = True
                return HttpResponseRedirect(reverse('copy'))
        elif request.POST.get('submit') == 'song':
            form = SongSearchForm(request.POST)
            if form.is_valid():  # Check if the form is valid.
                # Rate text here
                title = form.get_song_title()
                artist = form.get_song_artist()
                text = parsing.search_songs(title, artist)
                print(text)
            else:
                request.session['invalid_song'] = True
                return HttpResponseRedirect(reverse('search'))
        elif request.POST.get('submit') == 'tv_show':
            form = TVShowSearchForm(request.POST)
            if form.is_valid():
                print()
                # Rate text here
            else:
                request.session['invalid_tv_show'] = True
                return HttpResponseRedirect(reverse('search'))
        elif request.POST.get('submit') == 'movie':
            form = MovieSearchForm(request.POST)
            if form.is_valid():
                print()
                # Rate text here
            else:
                request.session['invalid_movie'] = True
                return HttpResponseRedirect(reverse('search'))
        elif request.POST.get('submit') == 'webpage':
            form = WebsiteSearchForm(request.POST)
            if form.is_valid():
                print()
                # Rate text here
            else:
                request.session['invalid_website'] = True
                return HttpResponseRedirect(reverse('search'))
        elif request.POST.get('submit') == 'file':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                handle_uploaded_file(request.FILES['file'])  # TODO This should be a temp file
                file = request.FILES['file'].name
                print(file)
                extension = file.split('.')[-1].lower()
                text = ''
                if extension == 'pdf':
                    text = parsing.parse_pdf('capstoneproject/tempfile')
                elif extension == 'epub':
                    text = parsing.parse_epub('capstoneproject/tempfile')
                elif extension == 'docx':
                    text = parsing.parse_docx('capstoneproject/tempfile')
                elif extension == 'txt':
                    text = parsing.parse_txt('capstoneproject/tempfile')
                print(text)
                os.remove('capstoneproject/tempfile')  # Delete the temp file after use
                # Parse file and rate text here
            else:
                return upload(request)
    return render(request, 'rating-result.html', context)





def handle_uploaded_file(f):
    with open('capstoneproject/tempfile', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required(login_url='/login/')
def compare_results(request):
    """
    Function to handle requests to compare rating results.
    :param request: The HTML request to handle.
    :return: Renders the compare page.
    """
    content_compare = request.session['content_compare']  # name of item to be compared, will be Content object in future
    request.session['delete'] = True
    current_category_ratings = dict()
    current_category_word_counts = dict()
    previous_category_ratings = dict()
    previous_category_word_counts = dict()
    for category in display_categories():
        current_category_ratings[category.name] = 5
        previous_category_ratings[category.name] = 8
        current_category_word_counts[category.name] = {'word1': 4,
                                                       'word2': 3,
                                                       'word3': 2
                                                       }
        previous_category_word_counts[category.name] = {'word1': 7,
                                                        'word2': 4,
                                                        'word3': 6
                                                        }
    context = {'current_name': 'Baby Got Back',
               'current_creator': 'Sir Mix a Lot',
               'previous_name': content_compare,
               'previous_creator': "Lil' Dicky (feat. BRAIN)",
               'current_overall_rating': 7,
               'previous_overall_rating': 5,
               'current_category_ratings': current_category_ratings,
               'current_category_word_counts': current_category_word_counts,
               'previous_category_ratings': previous_category_ratings,
               'previous_category_word_counts': previous_category_word_counts
               }
    return render(request, 'compare.html', context)


@login_required(login_url='/login/')
def word_counts(request, name):
    """
    Function to handle requests to the word counts page.
    :param request: The HTML request to handle.
    :return: Renders the word-counts page.
    """
    category_word_counts = dict()
    for category in display_categories():
        category_word_counts[category.name] = {'word1': 4,
                                               'word2': 3,
                                               'word3': 2
                                               }
    context = {'name': name,
               'category_word_counts': category_word_counts
               }
    return render(request, 'word-counts.html', context)
