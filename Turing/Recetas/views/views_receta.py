from typing import Any
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import CreateView,ListView
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView
from django.forms.models import model_to_dict 
from ..models import Receta, Cantidades_ingrediente ,Ingrediente
from ..forms import Form_Receta, Form_Cantidades
from Recetas.utils.funciones import decimal_to_float
class Lista_recetas_view(ListView):
    model = Receta 
    template_name = 'receta_tmp/list_recetas.html'
    context_object_name = 'lista_recetas'

def eliminar_session_data(request, id):
    ingredientes_dict = request.session.get('ingredientes_dict', {})
    ingrediente = ingredientes_dict.get(id)
    if ingrediente:
        del ingredientes_dict[id]
        request.session['ingredientes_dict'] = ingredientes_dict
    return redirect('crear_cant')
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
        action = request.POST.get('action')
        if action:
            receta_id = self.request.POST.get('receta_input')
            if receta_id:
                receta = get_object_or_404(Receta, id=int(receta_id))
                ingredientes_dict = request.session.get('ingredientes_dict', {})
            ingredientes_ids = {}
            for ingrediente_id, data in ingredientes_dict.items():
                cantidad = data['cantidad']
                ingrediente = Ingrediente.objects.get(id=ingrediente_id)
                if ingrediente.nombre_i not in ingredientes_ids:
                    ingredientes_ids[ingrediente.nombre_i] = [cantidad, ingrediente]
                cantidades_ingrediente = Cantidades_ingrediente(
                    nombre_ingrediente=ingrediente,
                    nombre_recete=receta,
                    cantidad=cantidad
                )
                cantidades_ingrediente.save()
            total_price = 0

            for _, ingrediente in ingredientes_ids.items():
                total_price += float(ingrediente[1].price_in_gr) * float(ingrediente[0])
            
            receta.costo_receta = total_price
            receta.save()
            request.session['ingredientes_dict'] = {}
            
            return redirect('lista_receta')
        
        ingredientes_dict = request.session.get('ingredientes_dict', {})
        
        ingrediente_id = request.POST.get('ingrediente_id')
        cantidad = request.POST.get('cantidad')
        
        if ingrediente_id and cantidad:
            cantidad = float(cantidad)
            ingrediente = Ingrediente.objects.get(id=ingrediente_id)

            ingrediente_dict = model_to_dict(ingrediente)
            ingrediente_dict = decimal_to_float(ingrediente_dict) 

            ingredientes_dict[ingrediente_id] = {
                'ingrediente': ingrediente_dict,
                'cantidad': cantidad
            }
        
        request.session['ingredientes_dict'] = ingredientes_dict
        
        return redirect('crear_cant')
    
        