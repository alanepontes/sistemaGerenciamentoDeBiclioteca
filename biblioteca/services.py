# -*- coding: utf-8 -*-

import django
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import Group

from biblioteca.models import *

def create_matricula_user(user):
    random.seed()
    num = random.randrange(999999)
    matricula = Matricula.objects.filter(numero=num)
    while matricula:
        num = random.randrange(999999)
        matricula = Matricula.objects.get(numero=num)
    matricula = Matricula.objects.get_or_create(user=user, numero=num)

def register_user(user_form, endereco_form, contato_form):
    user = user_form.save(commit=False)
    user.set_password(user.password)
    user.is_active = False
    user.save()

    endereco = endereco_form.save(commit=False)
    endereco.user = user
    endereco.save()

    contato = contato_form.save(commit=False)
    contato.user = user
    contato.save()
    
    create_matricula_user(user)
    
    group = Group.objects.get(name='leitor')
    user.groups.add(group)
    
    bibliotecarios = User.objects.filter(groups__name__in=['bibliotecario'])
    biblitecarios_email = [ b.email for b in bibliotecarios ]
    
    send_mail('Ativar usuário', 'Existe usuário para ser ativado.', 'alfredocdmiranda@gmail.com',
    bibliotecarios_email, fail_silently=False)
    
    return True