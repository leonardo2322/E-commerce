from django.urls import path
from .views import View_Crear_ingrediente

urlpatterns = [
    path('crear/ingrediente/',View_Crear_ingrediente.as_view(),name='crear_ingrediente')
]