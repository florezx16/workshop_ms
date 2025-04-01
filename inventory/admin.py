from django.contrib import admin
from .models import Inventory, InventoryCodes, InventoryMovement

# Register your models here.
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['code','available_quantity','updatetime','status']
    readonly_fields = ['createtime','updatetime','available_quantity','code']
    list_filter = ['status']
    ordering = ['code']
    search_fields = ['code','updatetime']
    
    def has_add_permission(self, request):
        return False

class InventoryCodesAdmin(admin.ModelAdmin):
    list_display = ['id','code','name','type','supplier','related_image','status']
    readonly_fields = ['createtime','updatetime']
    list_filter = ['status','type','supplier']
    ordering = ['code']
    search_fields = ['code','name']
    
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ['id','inventory_code','type','quantity','status','is_inbound','createtime']
    readonly_fields = ['createtime','inventory_code','quantity','type','is_inbound']
    list_filter = ['status','type']
    ordering = ['-id']
    search_fields = ['inventory_code']
    
    def has_add_permission(self, request):
        return False
    
admin.site.register(InventoryCodes, InventoryCodesAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(InventoryMovement, InventoryMovementAdmin)


