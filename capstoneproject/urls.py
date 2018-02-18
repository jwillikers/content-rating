"""capstoneproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import url

from capstoneproject.views import homepage
from capstoneproject.views import login
from capstoneproject.views import profile
from capstoneproject.views import search
from capstoneproject.views import upload
from capstoneproject.views import copy_in
from capstoneproject.views import about_algorithm
from capstoneproject.views import about_page
from capstoneproject.views import words

urlpatterns = [
    url(r'^admin/?', admin.site.urls),
    url(r'^login/?$', login, name='login'),
	url(r'^profile/?$', profile, name='profile'),
	url(r'^search/?$', search, name='search'),
	url(r'^upload/?$', upload, name='upload'),
	url(r'^copy/?$', copy_in, name='copy'),
	url(r'^algorithm/?$', about_algorithm, name='algorithm'),
	url(r'^about/?$', about_page, name='about'),
    url(r'^words/?$', words, name='words'),
    url(r'^/?$', homepage), # Main page, obviously
]
