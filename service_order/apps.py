from django.apps import AppConfig


class ServiceOrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'service_order'
    verbose_name = 'Service orders'
    
    def ready(self):
        import service_order.signals
