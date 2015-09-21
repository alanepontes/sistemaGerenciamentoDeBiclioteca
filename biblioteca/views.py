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

from datetime import datetime

from biblioteca.forms import *
from biblioteca.models import *
from biblioteca.services import *

#TODO Organizar e padronizar as views

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['settings'] = settings

        return context

def ListBooksView(request):
    material = Material.objects.all()
    
    if request.method == "POST":
        messages = []
        busca=request.POST['material']

        material = Material.objects.filter(nome__startswith=busca)
    #emprestimos = Emprestimo.objects.filter(data_devolucao=None)
    #dict_emprestimos = { e.livro.id: 0 for e in emprestimos }
    #for e in emprestimos:
    #    dict_emprestimos[e.livro.id] += 1
    #for b in books:
    #    b.quantidade_disponivel = b.quantidade - dict_emprestimos[b.id]
    return render_to_response("books.html",{"books": material}, context_instance=RequestContext(request))

def EmprestarView(request, pk):
    #user = User.objects.get(id=request.user.id)
    material = Material.objects.get(id=pk)
    #material.emprestar(request.user)
    if hasattr(material, 'livro'):
        material.livro.emprestar(request.user)
    return redirect("home")

class BookDetailView(DetailView):
    model = Material
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
        profile_form = ProfileForm(data=request.POST)
        endereco_form = EnderecoForm(data=request.POST)
        contato_form = ContatoForm(data=request.POST)
        
        if user_form.is_valid() and endereco_form.is_valid() and contato_form.is_valid() and profile_form.is_valid():
            if register_user(user_form, profile_form, endereco_form, contato_form):
                registered = True
        else:
            pass
            #print user_form.errors, endereco_form.errors, contato_form.errors

    else:
        user_form = UserForm()
        profile_form = ProfileForm()
        endereco_form = EnderecoForm()
        contato_form = ContatoForm()

    return render_to_response(
                'registration.html',
                {'user_form': user_form,
                 'profile_form': profile_form,
                 'endereco_form': endereco_form,
                 'contato_form': contato_form,
                 'registered': registered},
                context)

def CancelarRegistroView(request):
    if request.method == "POST":
        messages = []
        if request.POST["button"] == "sim":
            if not cancelar_registro(request.user):
                messages.append("Você não pode cancelar sua conta. Você deve possuir alguma pendência. Consulte um bibliotecário.")
                return render_to_response('cancelar.html',
                                          {'errors': messages},
                                          context_instance=RequestContext(request))
            logout(request)
            return redirect(reverse('home'))
        elif request.POST["button"] == "nao":
            return redirect(reverse('home'))
    
    return render_to_response('cancelar.html', context_instance=RequestContext(request))

def HistoricoView(request):
    historico = [ e for e in  Emprestimo.objects.filter(usuario=request.user.id) ]
    historico += [ r for r in Reserva.objects.filter(usuario=request.user.id) ]
    historico += [ r for r in Reclamacao.objects.filter(usuario=request.user.id) ]
    
    return render_to_response('historico.html', {"historico": historico}, context_instance=RequestContext(request))

def ReclamacaoView(request):
    context = RequestContext(request)
    done = False

    if request.method == 'POST':
        reclamacao_form = ReclamacaoForm(data=request.POST)
        
        if reclamacao_form.is_valid():
            if criar_reclamacao(reclamacao_form):
                done = True
        else:
            pass
    else:
        reclamacao_form = ReclamacaoForm()
        print reclamacao_form

    return render_to_response(
                'reclamacao.html',
                {'reclamacao_form': reclamacao_form,
                 'done': done},
                context)