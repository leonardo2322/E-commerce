from collections import defaultdict
import traceback

from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.urls import reverse
from django.views.generic import DetailView, View
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.db import transaction
from django.contrib import messages
from django.db.models import Prefetch

from ..models import  Product,Profile,Cart,Cart_Item, PurchaseHistory
from Products.utils.cart_utils import Cart_manage




class Show_product_view(LoginRequiredMixin,DetailView):
    model = Product
    template_name = 'Products/show_product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["cant"] = 1 
        return context
    

class Model_List_View(ListView):
    template_name = 'Cart_temp/cart_temp.html'
    context_object_name = 'cart_items'
    total = 0

    def get_queryset(self):
        cart = Cart_manage(self.request)
        cart.cart_total_price()
        if self.request.user.is_authenticated:
            return cart.cart.values()
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        cart = Cart_manage(self.request)
        total = cart.cart_total_price()
        context["total_cart"] = total
        return context
    



class Add_cart_view(View):
    

    def post(self, request, *args, **kwargs):
        product_id = self.request.POST.get('product_id')
        quantity = int(self.request.POST.get('quantity', 1))
        to_url = self.request.POST.get('to_url')
        product = get_object_or_404(Product, id=product_id)
        cart = Cart_manage(request)
        if quantity > 1:
            cart.add(product,quantity)
        else:
            cart.add(product)
        if to_url:
            url = reverse('products')
            return HttpResponseRedirect(url)
        
        url = reverse('show_product', kwargs={'pk': product.pk})
        return HttpResponseRedirect(url)
    
class Remove_item_cart(View):
    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        product = get_object_or_404(Product, id=product_id)
        cart = Cart_manage(request)
        cart.remove(product)
        
        url = reverse('cart')
        return HttpResponseRedirect(url)
    

    
class Sale_items_cart(View):
    
    def post(self, request,*args, **kwargs):
        cart = Cart_manage(request)
        try:
            with transaction.atomic():
                total_cart = cart.cart_total_price()

                cartbd = Cart.objects.filter(client=request.user.profile).first()
                if not cartbd:  # Si no existe un carrito, creamos uno nuevo
                    cartbd = Cart.objects.create(client=request.user.profile, total=total_cart)

                else:
                    cartbd.total = total_cart
                    cartbd.save()
                
                cart_items = cart.get_items()

                for item in cart_items:

                    product = Product.objects.get(id=item['id'])

                    if product.stock < int(item['cant']):
                        url = reverse('cart')
                        messages.error(request, "Stock insuficiente para el producto: " + product.name)
                        return HttpResponseRedirect(url,status=409)
                    
                    product.stock -= int(item['cant'])
                    product.save()

                    cartitem =Cart_Item.objects.create(
                        cart=cartbd,
                        prods=product,
                        cant = int(item['cant'])
                        )
                purchase = PurchaseHistory.objects.create(
                user=request.user.profile,
                cart=cartbd,
                total_price=cartbd.total,
                status="Complete"  # Cambiar si tienes diferentes estados
                ) 
                cartbd.complete_purchase()
                cart.clear()
        except Product.DoesNotExist:
            print("Producto no encontrado.")
            return HttpResponseRedirect(reverse('cart'), status=404)
        except Exception as e:
            print(str(e),"-----------este error")
            traceback.print_exc()
            return HttpResponseServerError(render(request, '500.html', status=500))
        
        return HttpResponseRedirect(reverse('products'))
        


class List_hystory_purchase(LoginRequiredMixin,ListView):
    model = PurchaseHistory
    template_name = 'Cart_temp/list_history.html'
    context_object_name = 'purchases'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            cart_items = Cart_Item.objects.select_related('prods') 
            
            purchase_history = PurchaseHistory.objects.filter(
                user=self.request.user.profile,
            ).prefetch_related(
                Prefetch('cart__items', queryset=cart_items)
            ).order_by('-created_at')
            return purchase_history
        else:
            return PurchaseHistory.objects.none()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchases = self.get_queryset()

        # Agrupar las compras por hora
        grouped_purchases = defaultdict(list)
        for purchase in purchases:
            purchase_time = purchase.created_at.strftime('%H:%M')  # Agrupar por hora y minuto
            grouped_purchases[purchase_time].append(purchase)
       
        detalles = {
                indice: {
                    'compra_id': compra.id,
                    'total_compra': compra.total_price,
                    'created_at': compra.created_at,
                    'estado': compra.status,
                    'detalles': [
                        {indice:{'name':item.prods.name,'cant': item.cant, 'price': item.prods.pvp}} 
                        for item in compra.cart.items.all() 
                        if str(indice) == str(item.created.strftime('%H:%M'))
                    ]
                }
                for indice, item_group in grouped_purchases.items()
                for compra in item_group
                if any(
                        str(indice) == str(compra.created_at.strftime('%H:%M'))  
                        for compra in item_group
                    )
                
            }
        print(detalles)

   

        context = {
                'purchases_dict': detalles,
            }
        return context