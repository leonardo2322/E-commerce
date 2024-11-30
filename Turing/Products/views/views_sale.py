from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, View
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from ..models import  Product,Profile
from Products.utils.cart_utils import Cart_manage

class Show_product_view(LoginRequiredMixin,DetailView):
    model = Product
    template_name = 'Products/show_product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["quantity"] = 1 
        return context
    

class Model_List_View(ListView):
    template_name = 'Cart_temp/cart_temp.html'
    context_object_name = 'cart_items'
    total = 0

    def get_queryset(self):
        cart = Cart_manage(self.request)
        cart.cart_total_price()
        if self.request.user.is_authenticated:
            user = self.request.user
            profile = Profile.objects.get(user=user)
            cart.load_from_db(profile)

        return cart.cart.values()
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        cart = Cart_manage(self.request)
        total = cart.cart_total_price()
        print(total)
        context["total_cart"] = total
        return context
    



class Add_cart_view(View):
    

    def post(self, request, *args, **kwargs):
        product_id = self.request.POST.get('product_id')
        quantity = int(self.request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)

        cart = Cart_manage(request)
        if quantity > 1:
            cart.add(product,quantity)
        else:
            cart.add(product)

       
        url = reverse('show_product', kwargs={'pk': product.pk})
        return HttpResponseRedirect(url)