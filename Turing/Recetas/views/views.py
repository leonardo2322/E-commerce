from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import CreateView,ListView
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView
from ..models import Ingrediente
from ..forms import Form_Ingrediente

class View_Crear_ingrediente(CreateView):
    model = Ingrediente
    form_class = Form_Ingrediente
    context_object_name = 'obj_ingrediente'
    template_name = 'crear_ingrediente.html'
    success_url = reverse_lazy('list_ingrediente')


class View_listar_ingrediente(ListView):
    model = Ingrediente
    template_name = 'listado_ingredientes.html'
    context_object_name = 'lista_ingredientes'

class View_Eliminar_ingrediente(View):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        ingrediente = get_object_or_404(Ingrediente, pk=item_id)
        ingrediente.delete()

        url = reverse('list_ingrediente')
        return HttpResponseRedirect(url)    
    
class Actualizar_ingrediente_view(UpdateView):
    
    model = Ingrediente
    template_name = 'actualizar_ingrediente.html'
    fields = '__all__'
    success_url = reverse_lazy('list_ingrediente')