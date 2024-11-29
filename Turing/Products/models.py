from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

from django.db import models

from accounts.models import Profile

# Create your models here.
gender_choices = (
    ('male','Masculino'),
    ('female','Femenino'),
)
class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cate = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True)
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=3)
    description = models.TextField(max_length=350,blank=True, null= True)
    created = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']



class Cart(models.Model):
    client = models.OneToOneField(Profile, on_delete=models.CASCADE)
    total = models.DecimalField(default=0.00,max_digits=9, decimal_places=3)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.client.user}"

    class Meta:
        verbose_name = 'carrito'
        ordering = ['id']

class Cart_Item(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    prods = models.ForeignKey(Product, on_delete=models.CASCADE)
    cant = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.prods.pvp * self.cant
    

    def __str__(self):
        return self.prods.name

    class Meta:
        verbose_name = 'Detalle de carrito'
        ordering = ['id']
