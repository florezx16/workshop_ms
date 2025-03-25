from django.db import models
from assets.models import Asset
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Status(models.IntegerChoices):
    enable = (1,'Activo')
    disabled = (0,'Inactivo')
    __empty__ = ('-- Estado --')
    
class MovementsTypes(models.IntegerChoices):
    type_in = (1,'In')
    type_out = (2,'Out')
    __empty__ = ('-- Tipo de movimiento --')

class InventoryCodes(models.Model):
    class IntentoryType(models.IntegerChoices):
        spare_part = (1,'Repuesto')
        ink = (2,'Tinta')
        other = (3,'Otro')
        __empty__ = ('-- Tipo --')
    
    code = models.CharField(verbose_name='Código', max_length=50, unique=True)
    name = models.CharField(verbose_name='Nombre', max_length=100)
    type = models.IntegerField(verbose_name='Tipo', choices=IntentoryType)
    supplier = models.ForeignKey(to=Asset, verbose_name='Proovedor', on_delete = models.PROTECT)
    inbound_price = models.FloatField(verbose_name='Precio venta', default=0)
    outbound_price = models.FloatField(verbose_name='Precio compra', default=0)
    extra_info = models.TextField(verbose_name='Información adicional')
    status = models.IntegerField(verbose_name='Estado',choices=Status.choices, default=Status.enable)
    createtime = models.DateTimeField(verbose_name='Fecha/hora de creación', auto_now_add=True) 
    updatetime = models.DateTimeField(verbose_name='Fecha/hora de modificación', auto_now=True)
    
    class Meta:
        verbose_name = "Code"
        verbose_name_plural = "Codes"
        ordering = ['code']

    def __str__(self):
        return f'{self.name}({self.code})'

class Inventory(models.Model):         
    code = models.ForeignKey(verbose_name='Código', to=InventoryCodes, on_delete=models.PROTECT)
    available_quantity = models.IntegerField(verbose_name='Cantidad disponible', default=0, blank=True)
    extra_info = models.TextField(verbose_name='Información adicional')
    status = models.IntegerField(verbose_name='Estado',choices=Status.choices, default=Status.enable)
    createtime = models.DateTimeField(verbose_name='Fecha/hora de creación', auto_now_add=True) 
    updatetime = models.DateTimeField(verbose_name='Fecha/hora de modificación', auto_now=True)

    class Meta:
        verbose_name = "Current stock" 
        verbose_name_plural = "Current stocks"
        ordering = ['code']

    def __str__(self):
        return f'{str(self.code)}' 
    
class InventoryMovement(models.Model):
    inventory_code = models.ForeignKey(Inventory, verbose_name='Código de inventario', on_delete=models.CASCADE)
    type = models.IntegerField(verbose_name='Tipo de movimiento', choices=MovementsTypes.choices)
    quantity = models.IntegerField(verbose_name='Cantidad involucrada',validators=[MinValueValidator(1),MaxValueValidator(999)])
    description = models.TextField(verbose_name='Descripción del movimiento')
    status = models.IntegerField(verbose_name='Estado',choices=Status.choices, default=Status.enable)
    createtime = models.DateTimeField(verbose_name='Fecha/hora de creación', auto_now_add=True) 
    is_inbound = models.BooleanField(verbose_name='Inbound flag', default=False)
    
    class Meta:
        verbose_name = "Movement"
        verbose_name_plural = "Movements"
        ordering = ['-id','-createtime']

    def __str__(self):
        return str(self.id)

