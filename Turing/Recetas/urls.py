from django.urls import path
from .views.views import View_Crear_ingrediente, View_listar_ingrediente,View_Eliminar_ingrediente ,Actualizar_ingrediente_view
from .views.views_receta import Crear_Receta_view, Lista_recetas_view,Eliminar_receta_view,Actualizar_receta_view,Cantidades_para_recetas,eliminar_session_data
urlpatterns = [
    path('crear/ingrediente/',View_Crear_ingrediente.as_view(),name='crear_ingrediente'),
    path('ingredientes/',View_listar_ingrediente.as_view(),name='list_ingrediente'),
    path('eliminar/ingrediente/<int:pk>/', View_Eliminar_ingrediente.as_view(), name='eliminar_ing'),
    path('actualizar/ingrediente/<int:pk>/', Actualizar_ingrediente_view.as_view(), name='actualizar_ing'),

    path('crear/Receta/',Crear_Receta_view.as_view(),name='crear_receta'),
    path('lista/Recetas/',Lista_recetas_view.as_view(),name='lista_receta'),
    path('eliminar/Receta/<int:pk>/',Eliminar_receta_view.as_view(),name='eliminar_receta'),
    path('actualizar/Receta/<int:pk>/',Actualizar_receta_view.as_view(),name='actualizar_receta'),

    path('crear/cantidades/',Cantidades_para_recetas.as_view(),name='crear_cant'),
    path('crear/cantidades/<int:pk>/',Cantidades_para_recetas.as_view(),name='save_cant'),
    
    path('eliminar_s/<str:id>',eliminar_session_data,name='eliminar_name'),
]