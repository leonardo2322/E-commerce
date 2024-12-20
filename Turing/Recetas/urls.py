from django.urls import path
from .views import View_Crear_ingrediente, View_listar_ingrediente,View_Eliminar_ingrediente ,Actualizar_ingrediente_view
urlpatterns = [
    path('crear/ingrediente/',View_Crear_ingrediente.as_view(),name='crear_ingrediente'),
    path('ingredientes/',View_listar_ingrediente.as_view(),name='list_ingrediente'),
    path('eliminar/ingrediente/<int:pk>/', View_Eliminar_ingrediente.as_view(), name='eliminar_ing'),

    path('actualizar/ingrediente/<int:pk>/', Actualizar_ingrediente_view.as_view(), name='actualizar_ing')
]