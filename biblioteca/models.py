# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

import random
from datetime import datetime, timedelta

from biblioteca.exceptions import *

#TOOD Organizar os modelos

#Usuario
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    matricula = models.IntegerField(blank=True, unique=True)
    data_nascimento = models.DateField()
    
    def create_matricula(self):
        random.seed()
        num = random.randrange(999999)
        profile = Profile.objects.filter(matricula=num)
        while profile:
            num = random.randrange(999999)
            profile = Profile.objects.get(matricula=num)
        self.matricula = num

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


#Material
class Material(models.Model):
    nome = models.CharField(max_length=50)
    autor = models.CharField(max_length=100)
    data_publicacao = models.DateField()
    descricao = models.TextField()
    quantidade = models.IntegerField(default=0)
    valor = models.DecimalField(max_digits=7, decimal_places=2)

class Livro(Material):
    isbn10 = models.CharField(max_length=10)
    isbn13 = models.CharField(max_length=13)
    best_seller = models.BooleanField()
    
    def emprestar(self, usuario):
        emprestimo_livro_user = Emprestimo.objects.filter(usuario=usuario.id, material=self.id, data_devolvida=None)
        quant_emprestimos_user = Emprestimo.objects.filter(usuario=usuario.id, data_devolvida=None)
        quant_emprestimo_livro = Emprestimo.objects.filter(material=self.id, data_devolvida=None)
        diff = datetime.now()-datetime.combine(usuario.profile.data_nascimento, datetime.min.time())
        data = datetime.now()
        if self.best_seller:
            data_devolucao = data + timedelta(weeks=2)
        else:
            data_devolucao = data + timedelta(weeks=3)
        
        if not emprestimo_livro_user:
            if self.quantidade - len(quant_emprestimo_livro) > 0:
                if diff.days/365 > 12:
                    if len(quant_emprestimos_user) < 5:
                        emprestimo = Emprestimo(usuario=usuario, material=self,
                                                data=data, data_devolucao=data_devolucao)
                        emprestimo.save()
                    else:
                        raise MaxEmprestimoError()
                else:
                    if len(quant_emprestimos_user) < 2:
                        emprestimo = Emprestimo(usuario=usuario, material=self,
                                                data=data, data_devolucao=data_devolucao)
                        emprestimo.save()
                    else:
                        raise MaxEmprestimoError()
            else:
                raise NoItensError()
        else:
            raise AlreadyEmprestimoError()
        
        return True
            
    def reservar(self, usuario):
        reservas = Reserva.objects.filter(usuario=usuario.id, material=self.id, ativa=True)
        if len(reservas) >= 1:
            raise BaseException("Você já possui uma reserva desse material")
        
        reserva = Reserva(usuario=usuario, material=self, data=datetime.now(), ativa=True)
        reserva.save()
        
        return True
            

    def __unicode__(self):
        return self.nome

class Audiovisual(Material):
    pass
    
    def emprestar(self, usuario):
        emprestimo_livro_user = Emprestimo.objects.filter(usuario=usuario.id, material=self.id, data_devolvida=None)
        quant_emprestimos_user = Emprestimo.objects.filter(usuario=usuario.id, data_devolvida=None)
        quant_emprestimo_livro = Emprestimo.objects.filter(material=self.id, data_devolvida=None)
        diff = datetime.now()-datetime.combine(usuario.profile.data_nascimento, datetime.min.time())
        data = datetime.now()
        data_devolucao = data + timedelta(weeks=2)
        
        if not emprestimo_livro_user:
            if self.quantidade - len(quant_emprestimo_livro) > 0:
                if diff.days/365 > 12:
                    if len(quant_emprestimos_user) < 5:
                        emprestimo = Emprestimo(usuario=usuario, material=self,
                                                data=data, data_devolucao=data_devolucao)
                        emprestimo.save()
                    else:
                        raise MaxEmprestimoError()
                else:
                    if len(quant_emprestimos_user) < 2:
                        emprestimo = Emprestimo(usuario=usuario, material=self,
                                                data=data, data_devolucao=data_devolucao)
                        emprestimo.save()
                    else:
                        raise MaxEmprestimoError()
            else:
                raise NoItensError()
        else:
            raise AlreadyEmprestimoError()
        
        return True
    
    def reservar(self, usuario):
        reservas = Reserva.objects.filter(usuario=usuario.id, material=self.id, ativa=True)
        if len(reservas) >= 1:
            raise BaseException("Você já possui uma reserva desse material")
        
        reserva = Reserva(usuario=usuario, material=self, data=datetime.now(), ativa=True)
        reserva.save()
        
        return True
    
    def __unicode__(self):
        return self.nome

class RevistaReferencia(Material):
    pass

    def emprestar(self, usuario):
        raise BaseException("Não pode locar Revistas e Referências.")
    
    def reservar(self, usuario):
        raise BaseException("Não pode reservar Revistas e Referências.")

    def __unicode__(self):
        return self.nome


#Emprestimos
class Emprestimo(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)
    material = models.ForeignKey(Material)
    data = models.DateTimeField()
    data_devolucao = models.DateTimeField(blank=True)
    data_devolvida = models.DateTimeField(null=True, blank=True)
    renovada = models.BooleanField(default=False)
    multa = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    
    def renovar(self):
        if not renovada:
            data_devolucao = data_devolucao + (data_devolucao-data)
            return True
        else:
            return False

class Reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)
    material = models.ForeignKey(Livro)
    data = models.DateTimeField()
    ativa = models.BooleanField(default=True)


#Pedido
class Pedido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='usuario')
    fornecedor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='fornecedor')
    material = models.ForeignKey(Material)
    quantidade = models.IntegerField()
    data = models.DateTimeField()

    def entregar(self, fornecedor, valor):
        entrega = Entrega.objects.get(pedido=self.id)

        if not entrega:
            entrega = Entrega(fornecedor=fornecedor, pedido=self,
                              data=datetime.now(), valor=valor, pago=False)
            entrega.save()

            return True
        else:
            return False

class Entrega(models.Model):
    fornecedor = models.ForeignKey(settings.AUTH_USER_MODEL)
    pedido = models.OneToOneField(Pedido)
    data = models.DateTimeField()
    valor = models.DecimalField(max_digits=7, decimal_places=2)
    pago = models.BooleanField()

    def pagar(self):
        if not self.pago:
            self.pago = True
        else:
            self.pago = False


#Reclamação
class Reclamacao(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)
    reclamacao = models.TextField(max_length=500)
    data = models.DateTimeField()
