
import os
from django.http import Http404
from django.views.generic import DetailView,UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .forms import Profile_Form
from .models import Profile
# Create your views here.
class Profile_user_view(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = 'accounts/accounts_profile.html'
    context_object_name = "profile"

    def get_object(self):
        # Retorna el usuario actualmente autenticado
        return self.request.user.profile

    
class Profile_Image_Update_View(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['image']  # Campos que queremos editar
    template_name = 'profile_image_form.html'
    context_object_name = 'profile'

    def get_object(self):
        # Retorna el perfil del usuario autenticado
        return self.request.user.profile

    def form_valid(self, form):
        # Guardamos el perfil y redirigimos al perfil del usuario
        form.save()
        return redirect('profile_user') 
    
class Profile_Image_Delete_View(LoginRequiredMixin, View):
    success_url = reverse_lazy('profile_user')

    def get_object(self):
        # Asegura que se obtiene el perfil del usuario logueado
        return self.request.user.profile

    def post(self, request, *args, **kwargs):
        # Eliminar solo la imagen asociada al perfil
        profile = self.get_object()

        if profile.image and os.path.isfile(profile.image.path):
            os.remove(profile.image.path)  # Borra el archivo físico
        profile.image = None  # Elimina la referencia a la imagen en el modelo
        profile.save()  # Guarda los cambios en la base de datos

        return redirect(self.success_url)
    

class Profile_update_view(LoginRequiredMixin,UpdateView):
    model = Profile
    form_class = Profile_Form
    template_name = 'accounts/update_profile.html'
    context_object_name = 'update_profile'
    success_url = reverse_lazy('profile_user')


    def dispatch(self, request, *args, **kwargs):
        # Verificamos si el perfil del usuario autenticado existe
        try:
            # Intentamos obtener el perfil del usuario logueado
            self.object = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            # Si el perfil no existe, lanzamos un Http404
            raise Http404("Perfil no encontrado.")
        
        # Si el perfil existe, continuamos con el flujo normal
        return super().dispatch(request, *args, **kwargs)
    def get_object(self):
        # El objeto ya se ha asignado en dispatch(), así que podemos devolverlo aquí
        return self.object

 
 

    def form_valid(self, form):
            profile = form.save(commit=False)  # No lo guardamos aún
            profile.user = self.request.user  # Asignamos el usuario logueado
            profile.save()  # Guardamos el perfil
            return redirect(self.success_url)  # Redirigimos al perfil del usuario
    

    def form_invalid(self, form):
        print("Formulario no válido. Errores:", form.errors)
        return self.render_to_response(self.get_context_data(form=form))
        
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print("dentra en invalid form")
            return self.form_invalid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Acceder al nombre del usuario
        context['user_name'] = self.object.user.username
        return context