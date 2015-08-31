from django.conf import settings
from django.views.generic.base import TemplateView, View
from django.template import RequestContext
from django.shortcuts import render_to_response

from biblioteca.models import Book

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['settings'] = settings

        return context

def ListBooksView(request):
    books = Book.objects.all()
    r = Reserva(id_usuario, id_livro)
    r = Reserva(id_usuario, id_livro)
    return render_to_response("books.html",{"books": books}, context_instance=RequestContext(request))
