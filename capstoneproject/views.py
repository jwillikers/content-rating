from django.shortcuts import render
from django.http import HttpResponse

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