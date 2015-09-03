from django.conf import settings
from django.views.generic.base import TemplateView, View
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView, DetailView

from biblioteca.models import *

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['settings'] = settings

        return context

def ListBooksView(request):
    books = Livro.objects.all()
    return render_to_response("books.html",{"books": books}, context_instance=RequestContext(request))

class UserProfileDetail(DetailView):
    model = UserProfile

class UserProfileUpdate(UpdateView):
    model = UserProfile
    fields = ('homepage',)

    def get(self, request, *args, **kwargs):
        assure_user_profile_exists(kwargs['pk'])
        return (super(UserProfileUpdate, self).
                get(self, request, *args, **kwargs))

