from django.contrib import admin
from .models import Category,Product, Sale,DetSale
# Register your models here.
admin.site.register(Sale)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(DetSale)
