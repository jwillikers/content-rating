from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf

from capstoneproject.forms import SignUpForm, LoginForm


def login(request):
    if request.method == 'POST':
        if request.POST.get('submit') == 'signup':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                auth_login(request, user)
                return render(request, 'homepage.html')
            else:
                return render(request, 'login.html', {'login_form': LoginForm, 'signup_form': form})

        if request.POST.get('submit') == 'login':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)
                if user is not None:
                    if user.is_active:
                        auth_login(request, user)
                        return redirect('homepage')
                    else:
                        login_form = LoginForm()
                        login_form.disabled_account_error()
                        return render(request, 'login.html', {'login_form': form, 'signup_form': SignUpForm()})
            return render(request, 'login.html', {'login_form': form, 'signup_form': SignUpForm()})
    else:
        c = {}
        c.update((csrf(request)))
        c.update(({'login_form':LoginForm, 'signup_form': SignUpForm}))
        return render_to_response('login.html', c)


def login_redirect(request):
    return redirect('login')


@login_required(login_url='/login/')
def homepage(request):
    return render(request, 'homepage.html')


def logout(request):
    logout(request)
    return render(request, 'login.html', {'login_form': LoginForm, 'signup_form': SignUpForm})


@login_required(login_url='/login/')
def profile(request):
	return render(request, 'profile.html')


@login_required(login_url='/login/')
def search(request):
	return render(request, 'search.html')


@login_required(login_url='/login/')
def upload(request):
	return render(request, 'upload.html')


@login_required(login_url='/login/')
def copy_in(request):
	return render(request, 'copy-in.html')


def about_algorithm(request):
	return render(request, 'algorithm.html')


def about_page(request):
	return render(request, 'about.html')

@login_required(login_url='/login/')
def words(request):
    return render(request, 'words.html')

@login_required(login_url='/login/')
def rating_results(request):
	return render(request, 'rating-result.html')

@login_required(login_url='/login/')	
def compare_results(request):
	return render(request, 'compare.html')
