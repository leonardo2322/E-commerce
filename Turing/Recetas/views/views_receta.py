from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import CreateView,ListView
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView

from ..models import Receta, Cantidades_ingrediente ,Ingrediente
from ..forms import Form_Receta, Form_Cantidades

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

class Cantidades_para_recetas(View):
    def get(self, request, *args, **kwargs):

        ingredientes_dict = request.session.get('ingredientes_dict', {})
        receta = Receta.objects.all()


        ingredientes = Ingrediente.objects.all()

        return render(request, 'crear_cantidades.html', {
            'recetas': receta,
            'ingredientes': ingredientes,
            'ingredientes_dict': ingredientes_dict  
        })
    def post(self, request, *args, **kwargs):
        receta_id = kwargs.get('pk')
        receta = get_object_or_404(Receta, id=receta_id)
        
        ingredientes_dict = request.session.get('ingredientes_dict', {})
        
        ingrediente_id = request.POST.get('ingrediente_id')
        cantidad = request.POST.get('cantidad')
        
        if ingrediente_id and cantidad:
            cantidad = float(cantidad)
            ingrediente = Ingrediente.objects.get(id=ingrediente_id)
            
            ingredientes_dict[ingrediente_id] = {
                'ingrediente': ingrediente,
                'cantidad': cantidad
            }
        
        request.session['ingredientes_dict'] = ingredientes_dict
        
        return redirect('agregar_ingredientes', receta_id=receta.id)