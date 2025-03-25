from django.contrib import admin
from .models import Asset

# Register your models here.
class AssetAdmin(admin.ModelAdmin):
    list_display = ['id','name','type','document_type','document_id','status']
    readonly_fields = ['createtime','updatetime']
    list_filter = ['status','type']
    ordering = ['name']
    search_fields = ['name','document_id']

admin.site.register(Asset, AssetAdmin)