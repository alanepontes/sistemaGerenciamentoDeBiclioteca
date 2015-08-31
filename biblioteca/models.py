from django.db import models

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
    pass

    def __unicode__(self):
        return self

class Devolucao(models.Model):
    emprestimo = models.ForeignKey(Emprestimo)
    data = models.DateTimeField()

    def __unicode__(self):
        return self

class Endereco(models.Model):
    pass

    def __unicode__(self):
        return self

class Contato(models.Model):
    pass

    def __unicode__(self):
        return self

class Pedido(models.Model):
    livro = models.ForeignKey(Livro)
    fornecedor = models.ForeignKey(User)
    data = models.DateTimeField()

    def __unicode__(self):
        return self
