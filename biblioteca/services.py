# -*- coding: utf-8 -*-

import django
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import Group

from biblioteca.models import *

def send_email_bibliotecarios(subject, message):
    bibliotecarios = User.objects.filter(groups__name__in=['bibliotecario'])
    bibliotecarios_email = [ b.email for b in bibliotecarios ]
    
    send_mail(subject, message, 'alfredocdmiranda@gmail.com',
    bibliotecarios_email, fail_silently=False)

def register_user(user_form, profile_form, endereco_form, contato_form):
    user = user_form.save(commit=False)
    user.set_password(user.password)
    user.is_active = False
    user.save()
    
    profile = profile_form.save(commit=False)
    profile.user = user
    profile.create_matricula()
    profile.save()

    endereco = endereco_form.save(commit=False)
    endereco.user = user
    endereco.save()

    contato = contato_form.save(commit=False)
    contato.user = user
    contato.save()
    
    group = Group.objects.get(name='leitor')
    user.groups.add(group)
    
    send_email_bibliotecarios('Ativar usuário', 'Existe usuário para ser ativado.')
    
    return True

def cancelar_registro(user):
    emprestimos = Emprestimo.objects.filter(data_devolucao=None, usuario=user)
    if emprestimos:
        return False
    else:
        print "Inativando usuario..."
        user.is_active = False
        user.save()
        return True

def criar_reclamacao(reclmacao_form):
    reclamacao = reclamacao_form.save(commit=False)
    reclamacao.usuario = request.user
    reclamacao.data = datetime.now()
    reclamacao.save()
    send_email_bibliotecarios("Existe uma reclamação", "Por favor verificar o motivo da reclamação.")
    
    return True