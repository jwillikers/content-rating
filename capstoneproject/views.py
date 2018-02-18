from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import LogInForm


@login_required
def homepage(request):
    return render(request, 'homepage.html')


def login(request):
    return render(request, 'login.html')


@login_required
def profile(request):
	return render(request, 'profile.html')


@login_required
def search(request):
	return render(request, 'search.html')


@login_required
def upload(request):
	return render(request, 'upload.html')


@login_required
def copy_in(request):
	return render(request, 'copy-in.html')


def about_algorithm(request):
	return render(request, 'algorithm.html')


def about_page(request):
	return render(request, 'about.html')


def logout_view(request):
    logout(request)


def attempt_login(request):
    username = request.POST['loginUsername']
    password = request.POST['loginPassword']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
#        else:
    # Return a 'disabled account' error message
    else:
    # Return an 'invalid login' error message.
#        if request.method == 'POST':
#        form = LogInForm(request.POST)
#        if form.is_valid():
#            return render(request, 'homepage.html')
#        else:
#            form = LogInForm()
        return render(request, 'login.html', {'form': form})