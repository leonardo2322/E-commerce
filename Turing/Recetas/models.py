from django.db import models
from django.utils.timezone import now


class Ingrediente(models.Model):
    nombre_i = models.CharField(verbose_name="Nombre ingrediente",max_length=50,unique=True)
    cantid = models.DecimalField(verbose_name="Cantidad ingrediente",max_digits=12, decimal_places=2)
    precio = models.DecimalField(verbose_name="Precio ingrediente",max_digits=12, decimal_places=2)
    unidad_m = models.CharField(verbose_name="Unidad de medida ingrediente",max_length=2, choices=[('kg', 'Kilogramos'), ('gr', 'Gramos')])
    fecha_creado = models.DateTimeField(verbose_name="Fecha creado ingrediente",default=now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']  
        verbose_name = 'Ingrediente'
        verbose_name_plural = 'Ingredientes'
        constraints = [
            models.CheckConstraint(check=models.Q(precio__gte=0), name='precio_positivo')
        ]
        indexes = [
            models.Index(fields=['nombre_i']),
            models.Index(fields=['updated_at']),
        ]
    @property
    def price_in_gr(self):
        if self.unidad_m == 'kg':
            return (self.precio / self.cantid) / 1000
        return self.precio / self.cantid
    
    def __str__(self):
        return self.nombre_i

class Receta(models.Model):
    nombre_r = models.CharField(verbose_name='nombre de la Receta',max_length=50,unique=True)
    cantidad_p_r = models.DecimalField(verbose_name='cantidad_producida_de_receta',max_digits=12, decimal_places=2)
    porcentaje_venta = models.IntegerField(verbose_name='Porcentaje de ganancia')
    precio = models.DecimalField(verbose_name='Precio que se quiere para venta',max_digits=12, decimal_places=2)
    unidades_x_r = models.DecimalField(verbose_name='Cantidad que arroja la receta',max_digits=12, decimal_places=2)
    cant_x_paquete = models.IntegerField(verbose_name='Unidades por paquete')
    costo_receta = models.DecimalField(verbose_name='Costo de la receta',max_digits=12, decimal_places=2,blank=True,default=0)
    empaque = models.DecimalField(verbose_name='Empaque del producto',decimal_places=2,max_digits=12,default=0.03)
    stiker = models.DecimalField(decimal_places=2,max_digits=12, verbose_name='Sticker para el empaque', default=0.03)
    fecha_creado = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']  
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'
      
        indexes = [
            models.Index(fields=['nombre_r']),
            models.Index(fields=['updated_at']),
        ]
    def __str__(self):
        return self.nombre_r
    
class Cantidades_ingrediente(models.Model):
    nombre_ingrediente = models.ForeignKey("Ingrediente", on_delete=models.CASCADE)
    nombre_recete = models.ForeignKey("Receta",on_delete=models.CASCADE)
    cantidad = models.DecimalField(verbose_name="cantidad Del ingrediente", max_digits=12, decimal_places=2)
    fecha_creado = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']  
        verbose_name = 'Cantidad_ingrediente'
        verbose_name_plural = 'Cantidad_ingredientes'
    
    def __str__(self):
        return f'Cantidad_De: {self.nombre_ingrediente.nombre_i}'