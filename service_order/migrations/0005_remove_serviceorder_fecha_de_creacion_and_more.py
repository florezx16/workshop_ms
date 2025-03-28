# Generated by Django 5.0.6 on 2025-02-06 18:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_order', '0004_alter_serviceorder_fecha_de_creacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceorder',
            name='Fecha de creacion',
        ),
        migrations.RemoveField(
            model_name='serviceorder',
            name='Fecha de ultima actualización',
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='createtime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Fecha de creacion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='updatetime',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha de ultima actualización'),
        ),
    ]
