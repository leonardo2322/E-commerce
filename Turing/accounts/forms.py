from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Introduce una dirección de correo válida.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class Profile_Form(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'location','email']
  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Accedemos al usuario relacionado (join implícito por OneToOneField)
            user = self.instance.user
            self.fields['email'].initial = user.email

    def clean(self):
        cleaned_data = super().clean()
        location = cleaned_data.get('location')
        image = cleaned_data.get('image')

        if image and not location:
            raise forms.ValidationError("La ubicación es obligatoria si se actualiza la imagen.")

        return cleaned_data