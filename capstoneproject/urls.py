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
from django.urls import include, re_path, re_path
from django.contrib.auth import views as auth_views

from capstoneproject.views import homepage
from capstoneproject.views import login
from capstoneproject.views import profile
from capstoneproject.views import search
from capstoneproject.views import upload
from capstoneproject.views import copy_in
from capstoneproject.views import about_algorithm
from capstoneproject.views import about_page
from capstoneproject.views import words
from capstoneproject.views import rating_results
from capstoneproject.views import compare_results
from capstoneproject.views import word_counts

urlpatterns = [
    re_path(r'^admin/?', admin.site.urls),
    re_path(r'^login/$', login, name='login'), # Page where the user logs in
    re_path(r'^logout/$', auth_views.logout, {'next_page': 'login/'}, name='logout'),  # Page that logs the user out
    re_path(r'^profile/?$', profile, name='profile'),  # Page containing info about the user's profile
    re_path(r'^search/?$', search, name='search'),  # Page where the user can search for content to rate from online sources
    re_path(r'^upload/?$', upload, name='upload'),  # Page where the user can upload a file
    re_path(r'^copy/?$', copy_in, name='copy'),  # Page where the user can copy in text
    re_path(r'^algorithm/?$', about_algorithm, name='algorithm'),  # Page to describe the content rating algorithm
    re_path(r'^about/?$', about_page, name='about'),  # Page to describe the website
    re_path(r'^words/?$', words, name='words'),  # Page to show offensive words for the user to update
    re_path(r'^results/?$', rating_results, name='results'),  # Page to show the ratings results of one source
    re_path(r'^compare/?$', compare_results, name='compare'),  # Page to compare rating results from two sources
    re_path(r'^word-counts/?$', word_counts, name='word-counts'),  # Page to show counts of flagged words after rating
    re_path(r'', homepage, name='homepage'),  # Main page
]
