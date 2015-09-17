from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from biblioteca.models import *

class MatriculaInline(admin.StackedInline):
    model = Matricula
    can_delete = False

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('numero', )
        return self.readonly_fields

class EnderecoInline(admin.StackedInline):
    model = Endereco
    can_delete = False
    extra = 1


class UserAdmin(ModelAdmin):
    inlines = (MatriculaInline, EnderecoInline, )

admin.site.register(Livro)
admin.site.register(Reserva)
admin.site.register(Emprestimo)
#admin.site.register(Devolucao)
admin.site.register(Pedido)
admin.site.register(Endereco)
#admin.site.register(UserProfile, UserProfileAdmin)
#admin.site.register(UserProfile)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

