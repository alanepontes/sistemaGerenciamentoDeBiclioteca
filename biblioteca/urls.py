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
    url(r'^$', IndexView, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cancelar/$', CancelarRegistroView, name='cancelar'),
    url(r'^emprestar/(?P<pk>[0-9]+)/$', EmprestarView, name='emprestar'),
    url(r'^historico/$', HistoricoView, name='historico'),
    url(r'^login/$', LoginView, name='login'),
    url(r'^logout/$', LogoutView, name='logout'),
    url(r'^materials/', MaterialListView, name='materials'),
    url(r'^material/(?P<pk>[0-9]+)/$', MaterialDetailView, name='material'),
    url(r'^pedidos/$', PedidoListView, name='pedidos'),
    url(r'^pedido/(?P<pk>[0-9]+)/$', PedidoDetailView, name='pedido'),
    url(r'^reclamacao/$', ReclamacaoView, name='reclamacao'),
    url(r'^register/$', RegistrationView, name='registration'),
    url(r'^reservar/(?P<pk>[0-9]+)/$', ReservarView, name='reservar'),
]
