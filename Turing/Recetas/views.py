from django.shortcuts import render
from django.views.generic import CreateView
from .models import Ingrediente
from .forms import Form_Ingrediente

class View_Crear_ingrediente(CreateView):
    model = Ingrediente
    form_class = Form_Ingrediente
    context_object_name = 'obj_ingrediente'
    template_name = 'crear_ingrediente.html'