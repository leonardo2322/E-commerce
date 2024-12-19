from django import forms
from .models import Ingrediente, Cantidades_ingrediente, Receta

class Form_Ingrediente(forms.ModelForm):
    class Meta:
        model = Ingrediente
        exclude = ['updated_at']


class Form_Receta(forms.ModelForm):
    class Meta:
        model = Receta
        exclude = [ 'updated_at']

class Form_Cantidades(forms.ModelForm):
    class Meta:
        model = Cantidades_ingrediente
        exclude = [ 'updated_at']