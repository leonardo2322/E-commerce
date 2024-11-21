
import os
from django.views.generic import DetailView,UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
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
    fields = ['image','location']  # Campos que queremos editar
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

    def get_object(self):
        # Retorna el perfil del usuario autenticado
        user_profile = self.request.user.profile
        if not user_profile:
            raise ValueError("Perfil no encontrado.")
        return user_profile
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Acceder al nombre del usuario
        context['user_name'] = self.object.user.username
        return context

    def form_valid(self, form):
        # Guardamos el perfil y redirigimos al perfil del usuario
        print("Formulario es válido:", form.is_valid())
        if form.is_valid():
            print("Formulario es válido.")
            profile = form.save(commit=False)  # No guardamos aún
            print("Profile objeto antes de guardar:", profile)
            profile.user = self.request.user  # Asignamos el usuario logueado
            profile.save()  # Guardamos el perfil en la base de datos
            print("Perfil guardado con usuario:", profile.user)
            return redirect('profile_user')  # Redirigimos al perfil del usuario
        else:
            print("Formulario no válido. Errores:", form.errors)
            return self.render_to_response(self.get_context_data(form=form))
        
    def post(self, request, *args, **kwargs):
        # Verifica si el formulario se está enviando correctamente
        form = self.get_form()

        if form.is_valid():
            print("Formulario válido. Procediendo a guardar.")
            return self.form_valid(form)
        else:
            print("Formulario no válido. Errores:", form.errors)
            return self.form_invalid(form)