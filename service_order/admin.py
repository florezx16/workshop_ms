from django.contrib import admin
from .models import ServiceOrder, ServiceOrderImages, ServiceOrderConsumption

# Register your models here.
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ['id','serial','model','customer','flowStatus','createtime','status']
    readonly_fields = ['createtime','updatetime','diagnose_date','repair_date','cancel_date']
    list_filter = ['status','flowStatus']
    ordering = ['id']
    search_fields = ['serial','model','customer']

admin.site.register(ServiceOrder, ServiceOrderAdmin)
admin.site.site_title = "Gestión de Servicios"

class ServiceOrderImageAdmin(admin.ModelAdmin):
    list_display = ['id','service_order','flowStatus_related','image','createtime','status']
    readonly_fields = ['createtime','updatetime']
    list_filter = ['status']
    ordering = ['id']
    search_fields = ['id','service_order']

admin.site.register(ServiceOrderImages, ServiceOrderImageAdmin)
admin.site.site_title = "Evidencias de ordenes"

class ServiceOrderConsumptionAdmin(admin.ModelAdmin):
    list_display = ['id','service_order','inventory_code','quantity','unit_price','total','createtime','status']
    readonly_fields = ['createtime']
    list_filter = ['status']
    ordering = ['id']
    search_fields = ['id','service_order','inventory_code']

admin.site.register(ServiceOrderConsumption, ServiceOrderConsumptionAdmin)
admin.site.site_title = "Consumo en ordenes de servicio"