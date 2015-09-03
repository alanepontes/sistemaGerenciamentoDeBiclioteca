from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from registration.signals import user_registered

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    homepage = models.URLField()

def assure_user_profile_exists(pk):
    """
    Creates a user profile if a User exists, but the
    profile does not exist.  Use this in views or other
    places where you don't have the user object but have the pk.
    """
    user = User.objects.get(pk=pk)
    try:
        # fails if it doesn't exist
        userprofile = user.userprofile
    except UserProfile.DoesNotExist, e:
        userprofile = UserProfile(user=user)
        userprofile.save()
    return


def create_user_profile(**kwargs):
    UserProfile.objects.get_or_create(user=kwargs['user'])

user_registered.connect(create_user_profile)

class Livro(models.Model):
    nome = models.CharField(max_length=50)
    isbn10 = models.CharField(max_length=10)
    isbn13 = models.CharField(max_length=13)
    data_publicacao = models.DateField()
    descricao = models.TextField()

    def __unicode__(self):
        return self.nome

class Reserva(models.Model):
    usuario = models.ForeignKey(User)
    livro = models.ForeignKey(Livro)
    data = models.DateTimeField()

    def __unicode__(self):
        return self

class Emprestimo(models.Model):
    usuario = models.ForeignKey(User)
    livro = models.ForeignKey(Livro)
    data = models.DateTimeField()

    def __unicode__(self):
        return self

class Devolucao(models.Model):
    emprestimo = models.ForeignKey(Emprestimo)
    data = models.DateTimeField()

    def __unicode__(self):
        return self

#class Endereco(models.Model):
#    pass
#
#    def __unicode__(self):
#        return self

#class Contato(models.Model):
#    pass
#
#    def __unicode__(self):
#        return self

class Pedido(models.Model):
    livro = models.ForeignKey(Livro)
    fornecedor = models.ForeignKey(User)
    data = models.DateTimeField()

    def __unicode__(self):
        return self
