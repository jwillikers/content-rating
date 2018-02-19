from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import LogInForm


def homepage(request):
    return render(request, 'homepage.html')


def login(request):
    return render(request, 'login.html')


def profile(request):
	return render(request, 'profile.html')


def search(request):
	return render(request, 'search.html')


def upload(request):
	return render(request, 'upload.html')


def copy_in(request):
	return render(request, 'copy-in.html')


def about_algorithm(request):
	return render(request, 'algorithm.html')


def about_page(request):
	return render(request, 'about.html')


def words(request):
    return render(request, 'words.html')
	
	
def rating_results(request):
	return render(request, 'rating-result.html')

	
def compare_results(request):
	return render(request, 'compare.html')
