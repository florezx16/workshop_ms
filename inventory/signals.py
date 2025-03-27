from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Inventory,InventoryMovement

@receiver(post_save,sender=InventoryMovement)
def modifyQuantity(sender,instance,created,**kwargs):
    print('START: *** Signal execution - #001(Inbound) ***')
    #sender = Modelo(desde donde se "escucha")
    #instance = Instancia del modelo en cuestion (donde se escucho)
    #created = Define si se creo o no(Booleano)
    #kwargs = parametros adicionales
    
    #Only process the requeust if the creation was successfully
    if not created:
        print('\tNot executed, record not found')
        print('END: *** Signal execution - #001(Inbound) ***')
        return None
    
    #Only process the requeust if was inbound movement
    if not instance.is_inbound:
        print('\tNot executed, not inbound movement')
        print('END: *** Signal execution - #001(Inbound) ***')
        return None
    
    try:        
        #Get inventory instance
        inventoryInstance = Inventory.objects.get(id=instance.inventory_code_id)
        print(f'\tOld stock:{inventoryInstance.available_quantity}')
        print(f'\tStock2Add:{instance.quantity}')
        
        #Update the available quantity
        inventoryInstance.available_quantity += instance.quantity
        print(f'\tStock updated:{inventoryInstance.available_quantity}')
        
        inventoryInstance.save()
        print('\tSaving update...')
    except Inventory.DoesNotExist:
        print('ERROR: Inventory instance not found.')
    except Exception as e:
        print(f'ERROR({type(e).__name__}):{e}')
    print('END: *** Signal execution - #001(Inbound) ***')
    