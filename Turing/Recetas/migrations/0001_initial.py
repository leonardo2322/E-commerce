# Generated by Django 5.1.3 on 2024-12-19 18:01

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingrediente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_i', models.CharField(max_length=50)),
                ('cantid', models.DecimalField(decimal_places=2, max_digits=12)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=12)),
                ('unidad_m', models.CharField(choices=[('kg', 'Kilogramos'), ('gr', 'Gramos')], max_length=2)),
                ('fecha_creado', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Ingrediente',
                'verbose_name_plural': 'Ingredientes',
                'ordering': ['-updated_at'],
                'indexes': [models.Index(fields=['nombre_i'], name='Recetas_ing_nombre__3521fc_idx'), models.Index(fields=['updated_at'], name='Recetas_ing_updated_bc3bb3_idx')],
                'constraints': [models.CheckConstraint(condition=models.Q(('precio__gte', 0)), name='precio_positivo')],
            },
        ),
        migrations.CreateModel(
            name='Receta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_r', models.CharField(max_length=50, verbose_name='nombre de la Receta')),
                ('cantidad_p_r', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='cantidad_producida_de_receta')),
                ('porcentaje_venta', models.IntegerField(verbose_name='Porcentaje de venta')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Precio que se quiere para venta')),
                ('unidades_x_r', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Cantidad que arroja la receta')),
                ('cant_x_paquete', models.IntegerField(verbose_name='Unidades por paquete')),
                ('costo_receta', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, verbose_name='Costo de la receta')),
                ('empaque', models.DecimalField(decimal_places=2, default=0.03, max_digits=12, verbose_name='Empaque del producto')),
                ('stiker', models.DecimalField(decimal_places=2, default=0.03, max_digits=12, verbose_name='Sticker para el empaque')),
                ('fecha_creado', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Receta',
                'verbose_name_plural': 'Recetas',
                'ordering': ['-updated_at'],
                'indexes': [models.Index(fields=['nombre_r'], name='Recetas_rec_nombre__b3bc06_idx'), models.Index(fields=['updated_at'], name='Recetas_rec_updated_4dfec5_idx')],
            },
        ),
        migrations.CreateModel(
            name='Cantidades_ingrediente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='cantidad Del ingrediente')),
                ('fecha_creado', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nombre_ingrediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Recetas.ingrediente')),
                ('nombre_recete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Recetas.receta')),
            ],
            options={
                'verbose_name': 'Cantidad_ingrediente',
                'verbose_name_plural': 'Cantidad_ingredientes',
                'ordering': ['-updated_at'],
            },
        ),
    ]
