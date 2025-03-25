# Generated by Django 5.1.2 on 2024-11-19 19:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assets', '0003_alter_asset_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(max_length=50, verbose_name='Numero de serie')),
                ('model', models.CharField(max_length=50, verbose_name='Modelo')),
                ('registry_comments', models.TextField(verbose_name='Observaciones iniciales')),
                ('registry_date', models.DateTimeField(max_length=50, verbose_name='Fecha de registro')),
                ('status', models.IntegerField(choices=[(None, '-- Estado --'), (1, 'Activo'), (0, 'Inactivo')], default=1, verbose_name='Estado')),
                ('Fecha de creacion', models.DateTimeField(auto_now_add=True, max_length=50)),
                ('Fecha de ultima actualización', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assets.asset', verbose_name='Cliente')),
            ],
            options={
                'verbose_name': 'Service orders',
                'verbose_name_plural': 'Service orders',
                'ordering': ['id'],
            },
        ),
    ]
