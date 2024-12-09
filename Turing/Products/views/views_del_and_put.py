from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import  UpdateView
from Products.models import Category, Product
from django.views.generic import  View


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
    fields = ['name', 'cate', 'image', 'pvp', 'description', 'stock']
    success_url = reverse_lazy('list_Product')

    def get_form(self):
        form = super().get_form()
        form.initial = {
                'name': form.instance.name,
                'cate': form.instance.cate,
                'image': form.instance.image,
                'pvp': form.instance.pvp,
                'description': form.instance.description,
                'stock': form.instance.stock,
            }
        form.instance = self.get_object()
        print(form.instance,"sassadssad")
        for field_name, field in form.fields.items():
            if field.widget.__class__.__name__ == 'Textarea':  # Si el widget es un textarea
                field.widget.attrs.update({
                    'class': 'form-control',  # Clase Bootstrap
                    'style': 'height: 100px; width: 100%; resize: vertical;',  # Tamaño ajustable
                    'placeholder': 'Ingresa una descripción breve...'  # Placeholder
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control',  # Clase estándar para otros inputs
                })
        print(form.initial,"sassadssad")
        
        return form