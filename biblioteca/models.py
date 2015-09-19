# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

import random

#TODO Criar o número de matrícula após o usuário ser cadastrado
#TODO Colocar a função de matrícula em algum lugar como "services"
#TOOD Organizar os modelos

class Matricula(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    numero = models.IntegerField(unique=True)

#class UserProfile(models.Model):
#    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
#   homepage = models.URLField()

#def assure_user_profile_exists(pk):
#    """
#    Creates a user profile if a User exists, but the
#    profile does not exist.  Use this in views or other
#    places where you don't have the user object but have the pk.
#    """
#    user = User.objects.get(pk=pk)
#    try:
#        # fails if it doesn't exist
#        userprofile = user.userprofile
#    except UserProfile.DoesNotExist, e:
#        userprofile = UserProfile(user=user)
#        userprofile.save()
#    return

class Livro(models.Model):
    nome = models.CharField(max_length=50)
    isbn10 = models.CharField(max_length=10)
    isbn13 = models.CharField(max_length=13)
    data_publicacao = models.DateField()
    descricao = models.TextField()
    quantidade = models.IntegerField(default=0)

    def __unicode__(self):
        return self.nome

class Reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)
    livro = models.ForeignKey(Livro)
    data = models.DateTimeField()
    ativa = models.BooleanField(default=True)

class Emprestimo(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)
    livro = models.ForeignKey(Livro)
    data = models.DateTimeField()
    data_devolucao = models.DateTimeField(null=True, blank=True)

class Endereco(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=50)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=50)

class Contato(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    contato = models.CharField(max_length=15)
    descricao = models.CharField(max_length=100)

class Pedido(models.Model):
    livro = models.ForeignKey(Livro)
    fornecedor = models.ForeignKey(User)
    data = models.DateTimeField()
