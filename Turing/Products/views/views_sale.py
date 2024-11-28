from ..models import  Product
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

class Show_product_view(LoginRequiredMixin,DetailView):
    model = Product
    template_name = 'Products/show_product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["quantity"] = 1 
        return context
    
