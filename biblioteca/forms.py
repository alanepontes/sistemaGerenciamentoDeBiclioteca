from django import forms
from django.contrib.auth.models import User

from biblioteca.models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['data_nascimento']

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['rua', 'numero', 'bairro', 'cep', 'cidade']

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['contato', 'descricao']

class ReclamacaoForm(forms.ModelForm):
    class Meta:
        model = Reclamacao
        fields = ['reclamacao']

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['fornecedor', 'material', 'quantidade']

class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = ['valor']
