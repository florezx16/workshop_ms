from django.contrib import admin
from .models import Inventory, InventoryCodes, InventoryMovement, InventoryCategory

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
    list_display = ['id','code','name','category','supplier','related_image','status']
    readonly_fields = ['createtime','updatetime']
    list_filter = ['status','supplier']
    ordering = ['code']
    search_fields = ['code','name','category']
    
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ['id','inventory_code','type','quantity','status','is_inbound','createtime']
    readonly_fields = ['createtime','inventory_code','quantity','type','is_inbound']
    list_filter = ['status','type']
    ordering = ['-id']
    search_fields = ['inventory_code']
    
    def has_add_permission(self, request):
        return False
    
class InventoryCategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','status','createtime','updatetime']
    readonly_fields = ['createtime','updatetime']
    list_filter = ['status']
    ordering = ['id','-createtime','name']
    search_fields = ['name']
    
admin.site.register(InventoryCodes, InventoryCodesAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(InventoryMovement, InventoryMovementAdmin)
admin.site.register(InventoryCategory, InventoryCategoryAdmin)



