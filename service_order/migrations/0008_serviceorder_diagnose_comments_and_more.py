# Generated by Django 5.0.6 on 2025-02-10 13:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_order', '0007_serviceorder_flowstatus_serviceorderimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceorder',
            name='diagnose_comments',
            field=models.TextField(default='', verbose_name='Observaciones'),
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='diagnose_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de diagnóstico'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='serviceorder',
            name='createtime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='serviceorderimages',
            name='createtime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación'),
        ),
    ]
