from django.shortcuts import render
from django.http import HttpResponse

def homepage(request):
	return render(request, 'homepage.html')
    
def login(request):
    return render(request, 'login.html')