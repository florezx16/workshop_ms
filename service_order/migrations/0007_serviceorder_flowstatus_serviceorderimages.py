# Generated by Django 5.0.6 on 2025-02-07 18:32

import django.db.models.deletion
import service_order.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_order', '0006_remove_serviceorder_registry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceorder',
            name='flowStatus',
            field=models.IntegerField(choices=[(None, '-- Estado de la orden --'), (1, 'En diagnostico'), (2, 'En reparacion'), (3, 'Completada'), (4, 'Cancelada')], default=1, verbose_name='Estado de la orden'),
        ),
        migrations.CreateModel(
            name='ServiceOrderImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=service_order.utils.get_serviceOrder_imagePath, verbose_name='Imagenes')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
                ('status', models.IntegerField(choices=[(None, '-- Estado --'), (1, 'Activo'), (0, 'Inactivo')], default=1, verbose_name='Estado')),
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name='Fecha de ultima actualización')),
                ('service_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service_order.serviceorder', verbose_name='Orden de servicio')),
            ],
        ),
    ]
