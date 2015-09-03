from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from biblioteca.models import *

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

admin.site.register(Livro)
admin.site.register(Reserva)
admin.site.register(Emprestimo)
admin.site.register(Devolucao)
admin.site.register(Pedido)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

