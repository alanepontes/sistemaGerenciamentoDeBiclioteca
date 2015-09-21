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
    url(r'^cancelar/$', CancelarRegistroView, name='cancelar'),
    url(r'^emprestar/(?P<pk>[0-9]+)/$', login_required(EmprestarView), name='emprestar'),
    url(r'^historico/$', login_required(HistoricoView), name='historico'),
    url(r'^reclamacao/$', login_required(ReclamacaoView), name='reclamacao'),
    url(r'^login/$', LoginView, name='login'),
    url(r'^logout/$', LogoutView, name='logout'),
    url(r'^register/$', RegistrationView, name='registration'),
    url(r'^reservar/(?P<pk>[0-9]+)/$', login_required(ReservarView), name='reservar'),
    url(r'^books/', login_required(ListBooksView), name='books'),
    url(r'^book/(?P<pk>[0-9]+)/$', login_required(BookDetailView.as_view()), name='book_detail'),
]
