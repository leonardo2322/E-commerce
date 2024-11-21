from django import forms
from .models import Profile


class Profile_Form(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'image', 'location']
        widgets = {
            'user': forms.HiddenInput(),  # Este campo será oculto en el formulario
        }

    def __init__(self, *args, **kwargs):
        # Hacemos que el campo 'user' no sea editable, y lo asignamos al usuario logueado
        print("Formulario es válido: -----------")
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['user'].initial = self.instance.user