# -*- coding: utf-8 -*-

from django.conf import settings
from django.views.generic.base import TemplateView, View
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.views.generic import CreateView, UpdateView, DetailView, View

from datetime import datetime

from biblioteca.forms import *
from biblioteca.models import *
from biblioteca.services import *

#TODO Organizar e padronizar as views

@login_required
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
    
    return render_to_response('cancelar_registro.html', context_instance=RequestContext(request))

@login_required
def EmprestarView(request, pk):
    material = Material.objects.get(id=pk)
    messages = []
    try:
        if hasattr(material, 'livro'):
            material.livro.emprestar(request.user)
        elif hasattr(material, 'audiovisual'):
            material.audiovisual.emprestar(request.user)
        elif hasattr(material, 'revistareferencia'):
            material.revistareferencia.emprestar(request.user)
    except NoItensError as e:
        return render_to_response("reservar.html", {"object": material, "errors": messages}, context_instance=RequestContext(request))
    except MaxEmprestimoError as e:
        messages.append("Já possui máximo de itens emprestados.")
        return render_to_response("material.html", {"object": material, "errors": messages}, context_instance=RequestContext(request))
    except AlreadyEmprestimoError as e:
        messages.append("Você já possue esse livro em mãos.")
        return render_to_response("material.html", {"object": material, "errors": messages}, context_instance=RequestContext(request))
    return redirect(reverse('home'))

@login_required
def IndexView(request):
    return render_to_response("index.html", context_instance=RequestContext(request))

@login_required
def HistoricoView(request):
    #TODO Organizar por data
    historico = [ i for i in  Emprestimo.objects.filter(usuario=request.user.id) ]
    historico += [ i for i in Reserva.objects.filter(usuario=request.user.id) ]
    historico += [ i for i in Reclamacao.objects.filter(usuario=request.user.id) ]
    
    return render_to_response('historico.html', {"historico": historico}, context_instance=RequestContext(request))

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
                messages.append('Conta não disponível.')
                return render_to_response('login.html', {'errors': messages}, context_instance=RequestContext(request))
        else:
            messages.append('Login ou senha incorreto.')
            return render_to_response('login.html', {'errors': messages}, context_instance=RequestContext(request))
        return redirect(reverse('home'))

    return render_to_response('login.html', context_instance=RequestContext(request))

def LogoutView(request):
    logout(request)
    return redirect(reverse('home'))

@login_required
def MaterialDetailView(request, pk):
    material = Material.objects.get(id=pk)
    return render_to_response("material_detail.html",{"object": material}, context_instance=RequestContext(request))

@login_required
def MaterialListView(request):
    materials = Material.objects.all()
    
    if request.method == "POST":
        messages = []
        busca=request.POST['material']

        materials = Material.objects.filter(nome__startswith=busca)
        
    return render_to_response("material_list.html",{"objects": materials}, context_instance=RequestContext(request))

@login_required
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

@login_required
def ReservarView(request, pk):
    material = Material.objects.get(id=pk)
    
    if hasattr(material, 'livro'):
        material.livro.reservar(request.user)
    elif hasattr(material, 'audiovisual'):
        material.audiovisual.reservar(request.user)
    elif hasattr(material, 'revistareferencia'):
        material.revistareferencia.reservar(request.user)
    return redirect(reverse("home"))

@login_required
def PedidoDetailView(request, pk):
    context = RequestContext(request)
    pedido = Pedido.objects.get(id=pk)

    if request.method == 'POST':
        entrega_form = EntregaForm(data=request.POST)
        
        if entrega_form.is_valid():
            pedido.entregar(request.user, request.POST['valor'])

            return redirect(reverse('home'))
    else:
        entrega_form = EntregaForm()
    
    return render_to_response('pedido_detail.html', {'object': pedido, 'entrega_form': entrega_form}, context)

@login_required
def PedidoListView(request):
    pedidos = Pedido.objects.filter(quantidade__gt = 0, usuario=request.user.id)
        
    return render_to_response("pedido_list.html",{"objects": pedidos}, context_instance=RequestContext(request))

@login_required
def PedidoView(request):
    context = RequestContext(request)
    done = False

    if request.method == 'POST':
        pedido_form = PedidoForm(data=request.POST)
        
        if pedido_form.is_valid():
            if fazer_pedido(pedido_form):
                done = True
    else:
        pedido_form = PedidoForm()

    return render_to_response(
                'pedido.html',
                {'pedido_form': pedido_form,
                 'done': done},
                context)
