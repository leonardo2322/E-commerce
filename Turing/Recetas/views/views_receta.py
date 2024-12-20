from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import CreateView,ListView
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView

from ..models import Receta
from ..forms import Form_Receta

class Lista_recetas_view(ListView):
    model = Receta 
    template_name = 'receta_tmp/list_recetas.html'
    context_object_name = 'lista_recetas'


class Crear_Receta_view(CreateView):
    model = Receta
    form_class = Form_Receta
    context_object_name = 'receta_creada'
    template_name = 'receta_tmp/crear_receta.html'
    
    success_url = reverse_lazy('lista_receta')


class Eliminar_receta_view(View):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        receta = get_object_or_404(Receta, pk=item_id)
        receta.delete()

        url = reverse('lista_receta')
        return HttpResponseRedirect(url)    


class Actualizar_receta_view(UpdateView):
    model = Receta
    template_name = 'receta_tmp/actualizar_receta.html'
    fields = '__all__'
    success_url = reverse_lazy('lista_receta')