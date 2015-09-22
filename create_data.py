# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group, Permission

from datetime import datetime
from biblioteca.models import *

#Creating groups
permissions = Permission.objects.all()
bibliotecario = Group(name='bibliotecario')
bibliotecario.save()
for p in permissions:
    bibliotecario.permissions.add(p)
bibliotecario.save()

fornecedor = Group(name='fornecedor')
fornecedor.save()
leitor = Group(name='leitor')
leitor.save()

# Creating superuser
username = "admin"
email = "alfredocdmiranda@gmail.com"
password = "123"

user = User(username=username, email=email, password=password)
user.set_password(password)
user.is_superuser = True
user.is_staff = True
user.save()
user.groups.add(bibliotecario)
user.save()
profile = Profile(user=user, data_nascimento=datetime(1990,7,9))
profile.create_matricula()
profile.save()

#Creating other users
u = User(username="user1", email="teste1@gmail.com", password="123")
u.set_password("123")
u.is_active=True
u.save()
u.groups.add(leitor)
u.save()
profile = Profile(user=u, data_nascimento=datetime(2005,7,9))
profile.create_matricula()
profile.save()
u = User(username="user2", email="teste2@gmail.com", password="123")
u.set_password("123")
u.is_active=True
u.save()
u.groups.add(leitor)
u.save()
profile = Profile(user=u, data_nascimento=datetime(2000,7,9))
profile.create_matricula()
profile.save()
u = User(username="user3", email="teste3@gmail.com", password="123")
u.set_password("123")
u.is_active=True
u.save()
u.groups.add(leitor)
u.save()
profile = Profile(user=u, data_nascimento=datetime(1995,7,9))
profile.create_matricula()
profile.save()
u = User(username="fornecedor1", email="fornecedor1@gmail.com", password="123")
u.set_password("123")
u.is_active=True
u.save()
u.groups.add(fornecedor)
u.save()
profile = Profile(user=u, data_nascimento=datetime(1995,7,9))
profile.create_matricula()
profile.save()
u = User(username="fornecedor2", email="fornecedor2@gmail.com", password="123")
u.set_password("123")
u.is_active=True
u.save()
u.groups.add(fornecedor)
u.save()
profile = Profile(user=u, data_nascimento=datetime(1995,7,9))
profile.create_matricula()
profile.save()

#Creating Material
m = Livro(nome="Harry Potter 1", autor="J.K.", data_publicacao=datetime(1997,05,01), descricao="Teste", quantidade=5, isbn10="1234567890", isbn13="1234567890123", best_seller=True, valor=50.50)
m.save()
m = Livro(nome="Harry Potter 2", autor="J.K.", data_publicacao=datetime(1998,05,01), descricao="Teste", quantidade=2, isbn10="0987654321", isbn13="0987654321098", best_seller=False, valor=76.50)
m.save()
m = Audiovisual(nome="Super video", autor="Desconhecido", data_publicacao=datetime(1985,10,15), descricao="Teste", quantidade=10, valor=150.00)
m.save()
m = RevistaReferencia(nome="Super revista", autor="Desconhecido da revista", data_publicacao=datetime(2011,10,15), descricao="Teste", quantidade=1, valor=0.50)
m.save()
    
