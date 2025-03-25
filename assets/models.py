from django.db import models

# Create your models here.
class Asset(models.Model):
    
    class AssetTypes(models.IntegerChoices):
        customer = (1,'Cliente')
        supplier = (2,'Proveedor')
        __empty__ = ('-- Tipo de Asset --')
        
    class AssetDocumentTypes(models.IntegerChoices):
        nit = (1,'NIT')
        local_id = (2,'CC')
        __empty__ = ('-- Tipo de documento --')
    
    class AssetStatus(models.IntegerChoices):
        enable = (1,'Activo')
        disable = (0,'Inactivo')
        
    name = models.CharField(verbose_name='Nombre',max_length=200)
    type = models.IntegerField(verbose_name='Tipo',choices=AssetTypes)
    document_type = models.IntegerField(verbose_name='Tipo de documento',choices=AssetDocumentTypes.choices)
    document_id = models.CharField(verbose_name='Numero de documento',max_length=200,unique=True)
    email = models.EmailField(verbose_name='Correo electrónico',max_length=200)
    phone = models.CharField(verbose_name='Teléfono de contacto',max_length=200)
    extra_info = models.TextField(verbose_name='Información adicional',max_length=500,blank=True)
    createtime = models.DateTimeField(verbose_name='Fecha/Hora de creación', auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name='Fecha/Hora ultima actualización', auto_now=True)
    status = models.IntegerField(verbose_name='Estado',choices=AssetStatus.choices,default=AssetStatus.enable)
    
    class Meta:
        verbose_name = 'Asset'
        verbose_name_plural = 'Assets'
        ordering = ['name']

    def __str__(self):
        return str(self.name)

