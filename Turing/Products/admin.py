from django.contrib import admin
from .models import Category,Product, Cart, Cart_Item
# Register your models here.
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart_Item)
