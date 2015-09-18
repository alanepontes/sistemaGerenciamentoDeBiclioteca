"""biblioteca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from biblioteca.views import *

#TODO Organizar URLs

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', login_required(IndexView.as_view()), name='home'),
    url(r'^login/$', LoginView, name='login'),
    url(r'^logout/$', LogoutView, name='logout'),
    url(r'^register/$', RegistrationView, name='registration'),
    url(r'^emprestar/(?P<pk>[0-9]+)/$', login_required(EmprestarLivroView), name='emprestar'),
    url(r'^books/', login_required(ListBooksView), name='books'),
    url(r'^book/(?P<pk>[0-9]+)/$', login_required(BookDetailView.as_view()), name='book_detail'),
#    url(r'^user/(?P<pk>[0-9]+)/$', UserProfileDetail.as_view(), name='user_profile_detail'),
#    url(r'^user/(?P<pk>[0-9]+)/update/$', UserProfileUpdate.as_view(), name='user_profile_edit'),
]
