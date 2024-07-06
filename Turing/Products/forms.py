from django.forms import ModelForm,TextInput
from .models import Category, Product



class FormCreateCategory(ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['autofocus'] = 'off'
    class Meta:
        model = Category
        fields = ['id', 'name']
        labels = {
            'name':'Nombre'
        }
        widgets= {
            'name': TextInput(attrs={
                "placeholder": "Ingrese el nombre de la categoria",
                'style':'width:17rem; margin: 10px 5px'
            })
        }

class FormCreateProduct(ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['autofocus'] = 'off'
    class Meta:
        model = Product
        fields = '__all__'
    def save(self, commit = True):
       data = {} 
       form = super()
       try:
           if form.is_valid():
               form.save()
           else:
               data['errors'] = form.errors
       except Exception as e:
           data['errors'] = form.errors
            
       return data