from django.db import models
from assets.models import Asset
from .utils import get_serviceOrder_imagePath
from inventory.models import Inventory

# Create your models here.    
class ServiceOrder_status(models.IntegerChoices):
    enable = (1,'Activo')
    disabled = (0,'Inactivo')
    __empty__ = ('-- Estado --')
    
class ServiceOrder_Flowtatus(models.IntegerChoices):
    pendingDiagnose = (1,'En diagnostico')
    onRepair = (2,'En reparacion')
    complete = (3,'Completada')
    cancel = (4,'Cancelada')
    __empty__ = ('-- Estado de la orden --')

class ServiceOrder(models.Model):
    customer = models.ForeignKey(verbose_name='Cliente',to=Asset, on_delete=models.PROTECT)
    serial = models.CharField(verbose_name='Numero de serie', max_length=50)
    model = models.CharField(verbose_name='Modelo', max_length=50)
    flowStatus = models.IntegerField(verbose_name='Estado de la orden',choices=ServiceOrder_Flowtatus.choices, default=ServiceOrder_Flowtatus.pendingDiagnose)
    registry_comments = models.TextField(verbose_name='Observaciones iniciales', blank=False)
    diagnose_date = models.DateTimeField(verbose_name='Fecha de diagnóstico', blank=False, null=True)
    diagnose_comments = models.TextField(verbose_name='Observaciones de diagnostico', blank=False, null=True)
    repair_date = models.DateTimeField(verbose_name='Fecha de reparación', blank=False, null=True)
    repair_comments = models.TextField(verbose_name='Observaciones de reparación', blank=False, null=True)
    cancel_date = models.DateTimeField(verbose_name='Fecha de cancelación', blank=False, null=True)
    cancel_comments = models.TextField(verbose_name='Motivo de cancelación', blank=False, null=True)
    consumables_total = models.FloatField(verbose_name='Total de consumibles', default=0)
    status = models.IntegerField(verbose_name='Estado',choices=ServiceOrder_status.choices, default=ServiceOrder_status.enable)
    services_total = models.FloatField(verbose_name='Total del servicio', default=0)
    services_description = models.TextField(verbose_name='Observaciones del servicio', blank=False, null=True)
    createtime = models.DateTimeField(verbose_name='Fecha de creación', auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name='Fecha de ultima actualización', auto_now=True)
        
    class Meta():
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['id']
    
    def __str__(self):
        return str(self.id)

class ServiceOrderImages(models.Model):
    service_order = models.ForeignKey(verbose_name='Orden de servicio', to=ServiceOrder, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Imagenes',upload_to=get_serviceOrder_imagePath)
    createtime = models.DateTimeField(verbose_name='Fecha de creación', auto_now_add=True)
    status = models.IntegerField(verbose_name='Estado',choices=ServiceOrder_status.choices, default=ServiceOrder_status.enable)
    updatetime = models.DateTimeField(verbose_name='Fecha de ultima actualización', auto_now=True)
    
    class Meta():
        verbose_name = "Attachment"
        verbose_name_plural = "Attachments"
        ordering = ['id']
    
class ServiceOrderConsumption(models.Model):
    service_order = models.ForeignKey(verbose_name='Orden de servicio', to=ServiceOrder, on_delete=models.CASCADE, limit_choices_to={'flowStatus':3,'status':1})
    inventory_code = models.ForeignKey(verbose_name='Codigo de inventario', to=Inventory, on_delete=models.PROTECT, limit_choices_to={'status':1})
    quantity = models.IntegerField(verbose_name='Cantidad')
    unit_price = models.FloatField(verbose_name='Precio unitario',null=True,blank=True)
    total = models.FloatField(verbose_name='Total',null=True,blank=True)
    createtime = models.DateTimeField(verbose_name='Fecha de creación', auto_now_add=True)
    status = models.IntegerField(verbose_name='Estado',choices=ServiceOrder_status.choices, default=ServiceOrder_status.enable)
    
    class Meta():
        verbose_name = "Consumption"
        verbose_name_plural = "Consumptions"
        ordering = ['id']