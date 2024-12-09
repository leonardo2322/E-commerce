from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import  UpdateView
from Products.models import Category, Product
from django.views.generic import  View
from Products.forms import Product_Form

class Category_Delete_View(View):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        category = get_object_or_404(Category, pk=item_id)

        category.delete()


        url = reverse('category_list')
        return HttpResponseRedirect(url)
    
class Category_update_view(UpdateView):
    model = Category
    template_name = 'Categoryes/update_categoy.html'
    fields = ['name']
    success_url = reverse_lazy('category_list')

class Product_delete_view(View):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        product = get_object_or_404(Product,pk=item_id)

        product.delete()

        url = reverse('list_Product')
        return HttpResponseRedirect(url)
    
class Product_update_view(UpdateView):
    model = Product
    template_name = "products/update_product.html"
    success_url = reverse_lazy('list_Product')
    form_class = Product_Form


    def form_valid(self, form):
        print("aqui")
        self.object = form.save()  # Guarda la instancia del modelo
        return HttpResponseRedirect(self.get_success_url())
            
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print("Errores del formulario:", form.errors)
        return response
    
    def get_form(self):
        form = super().get_form()
        product = self.get_object()
        if form.instance.pvp:
            form.instance.pvp = str(form.instance.pvp).replace(',', '')
        form.fields['cate'].initial = product.cate.pk
        form.initial = {
            'name': self.object.name,
            'cate': self.object.cate,
            'image': self.object.image,
            'pvp': self.object.pvp,
            'description': self.object.description,
            'stock': self.object.stock,
        }
        for field_name, field in form.fields.items():
            if field.widget.__class__.__name__ == 'Textarea':
                field.widget.attrs.update({
                    'class': 'form-control', 
                    'style': 'height: 100px; width: 100%; resize: vertical;', 
                    'placeholder': 'Ingresa una descripción breve...'  
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control',  
                })
        print("Valor inicial de cate (pk):", form.fields['cate'].initial)
        return form
  