from django import forms
from .models import Profile


class Profile_Form(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'location','email']
  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Accedemos al usuario relacionado (join implícito por OneToOneField)
            user = self.instance.user
      
            print("Usuario relacionado:", user.username)

    def clean(self):
        cleaned_data = super().clean()
        location = cleaned_data.get('location')
        image = cleaned_data.get('image')

        if image and not location:
            raise forms.ValidationError("La ubicación es obligatoria si se actualiza la imagen.")

        return cleaned_data