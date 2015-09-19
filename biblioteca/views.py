# -*- coding: utf-8 -*-

from django.conf import settings
from django.views.generic.base import TemplateView, View
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView, DetailView, View
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

from biblioteca.forms import *
from biblioteca.models import *
from biblioteca.services import *

#TODO Organizar e padronizar as views
#TODO Criar matrícula ao registrar usuário

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['settings'] = settings

        return context

def ListBooksView(request):
    books = Livro.objects.all()
    emprestimos = Emprestimo.objects.filter(data_devolucao=None)
    dict_emprestimos = { e.livro.id: 0 for e in emprestimos }
    for e in emprestimos:
        dict_emprestimos[e.livro.id] += 1
    for b in books:
        b.quantidade_disponivel = b.quantidade - dict_emprestimos[b.id]
    return render_to_response("books.html",{"books": books, "emprestimos": dict_emprestimos}, context_instance=RequestContext(request))

def EmprestarLivroView(request, pk):
    current_user = request.user
    print current_user.userprofile
    return redirect("home")

class BookDetailView(DetailView):
    model = Livro
    template_name = "book.html"

def LoginView(request):
    if request.method == "POST":
        messages = []
        user = authenticate(
                username=request.POST['username'],
                password=request.POST['password']
                )
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                messages.append('Account not available.')
                return render_to_response('login.html', {'errors': messages}, context_instance=RequestContext(request))
        else:
            messages.append('Password incorrect or account not available.')
            return render_to_response('login.html', {'errors': messages}, context_instance=RequestContext(request))
        return redirect(reverse('home'))

    return render_to_response('login.html', context_instance=RequestContext(request))

def LogoutView(request):
    logout(request)
    return redirect(reverse('home'))

def RegistrationView(request):
    context = RequestContext(request)
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        endereco_form = EnderecoForm(data=request.POST)
        contato_form = ContatoForm(data=request.POST)
        
        if user_form.is_valid() and endereco_form.is_valid() and contato_form.is_valid():
            if register_user(user_form, endereco_form, contato_form):
                registered = True
        else:
            pass
            #print user_form.errors, endereco_form.errors, contato_form.errors

    else:
        user_form = UserForm()
        endereco_form = EnderecoForm()
        contato_form = ContatoForm()

    return render_to_response(
                'registration.html',
                {'user_form': user_form,
                 'endereco_form': endereco_form,
                 'contato_form': contato_form,
                 'registered': registered},
                context)