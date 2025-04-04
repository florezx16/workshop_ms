# Generated by Django 5.1.5 on 2025-03-11 00:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_inventory_options_and_more'),
        ('service_order', '0011_serviceorder_cancel_comments_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceOrderConsumption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='Cantidad')),
                ('unit_price', models.FloatField(blank=True, null=True, verbose_name='Precio unitario')),
                ('total', models.FloatField(blank=True, null=True, verbose_name='Total')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('status', models.IntegerField(choices=[(None, '-- Estado --'), (1, 'Activo'), (0, 'Inactivo')], default=1, verbose_name='Estado')),
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name='Fecha de ultima actualización')),
                ('inventory_code', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.inventorycodes', verbose_name='Codigo de inventario')),
                ('service_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service_order.serviceorder', verbose_name='Orden de servicio')),
            ],
        ),
    ]
