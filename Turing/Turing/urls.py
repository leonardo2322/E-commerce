"""
URL configuration for Turing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import Profile_user_view,Profile_Image_Update_View,Profile_Image_Delete_View ,Profile_update_view
from django.conf.urls import handler404, handler500, handler403

def custom_500_view(request, exception=None):
    return render(request, '500.html', status=500)
def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)
def custom_403_view(request, exception=None):
    return render(request, '403.html', status=403)
handler403 = custom_403_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Products.urls')),
    path('recetas/',include('Recetas.urls')),
    path('accounts/',include("django.contrib.auth.urls")),
    path('accounts/profile/', Profile_user_view.as_view(), name="profile_user"),
    path('upload_image/', Profile_Image_Update_View.as_view(), name='upload_image'),
    path('eliminar-imagen/', Profile_Image_Delete_View.as_view(), name='delete_profile_image'),
    path('actualizar_perfil/',Profile_update_view.as_view(),name='update_profile')

]


urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)