from django.db import models
from inventory.models import Inventory

# Create your models here.
class Status(models.IntegerChoices):
    enable = (1,'Activo')
    disabled = (0,'Inactivo')
    __empty__ = ('-- Estado --')

class InventoryMovement(models.Model):
    inventory_code = models.ForeignKey(Inventory, verbose_name='Código de de inventario',on_delete=models.CASCADE)
    quanity = models.IntegerField(verbose_name='Cantidad afectada')
    description = models.TextField(verbose_name='Descripción del movimiento')
    status = models.IntegerField(verbose_name='Estado',choices=Status.choices, default=Status.enable)
    createtime = models.DateTimeField(verbose_name='Fecha/hora de creación', auto_now_add=True) 
    
    class Meta:
        verbose_name = "Inventory Movement"
        verbose_name_plural = "Inventory Movement"

    def __str__(self):
        return self.name

