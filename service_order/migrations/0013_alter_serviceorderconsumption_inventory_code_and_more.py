# Generated by Django 5.1.5 on 2025-03-11 00:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_inventory_options_and_more'),
        ('service_order', '0012_serviceorderconsumption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceorderconsumption',
            name='inventory_code',
            field=models.ForeignKey(limit_choices_to={'status': 1}, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.inventorycodes', verbose_name='Codigo de inventario'),
        ),
        migrations.AlterField(
            model_name='serviceorderconsumption',
            name='service_order',
            field=models.ForeignKey(limit_choices_to={'flowStatus': 3, 'status': 1}, on_delete=django.db.models.deletion.CASCADE, to='service_order.serviceorder', verbose_name='Orden de servicio'),
        ),
    ]
