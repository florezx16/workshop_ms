from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ServiceOrderConsumption
from inventory.models import Inventory
from core.utils import createMovementRecord

@receiver(post_save,sender=ServiceOrderConsumption)
def reduceQuantity_ConsumptionPanel(sender,instance,created,raw,using,update_fields,**kwargs):
    print('START: *** Signal execution - #002(ServiceOrder Consumption) ***')
    
    '''
    sender = Modelo(desde donde se "escucha")
    instance = Instancia del modelo en cuestion (donde se escucho)
    created = Define si se creo o no(Booleano)
    kwargs = parametros adicionales
    '''
    if not created:
        print('Not executed, record not found')
        print('END: *** Signal execution - #002(ServiceOrder Consumption) ***')
        return None
    try:
        print('Execution started')
        #Get inventory instance
        inventoryInstance = Inventory.objects.get(id=instance.inventory_code_id)
        print(f'Old stock:{inventoryInstance.available_quantity}')
        print(f'Stock2Reduce:{instance.quantity}')
        
        #Update the available quantity
        inventoryInstance.available_quantity -= instance.quantity
        print(f'Stock updated:{inventoryInstance.available_quantity}')
        
        inventoryInstance.save()
        print('Saving update...')
        
        #Create inventoryMovement record
        createMovementRecord(instance,2,f'Consumo de orden(Orden #{instance.service_order_id})') 
            
    except Inventory.DoesNotExist:
        print('ERROR: Inventory instance not found.')
    except Exception as e:
        print(f'ERROR({type(e).__name__}):{e}')
    print('END: *** Signal execution - #002(ServiceOrder Consumption) ***')
    
@receiver(post_delete,sender=ServiceOrderConsumption)
def rollBackQuantity_ConsumptionPanel(sender,instance,using,origin,**kwargs):
    print('START: *** Signal execution #003(ServiceOrder Consumption rollback) ***')
    
    '''
    sender = Modelo(desde donde se "escucha")
    instance = Instancia del modelo en cuestion (donde se escucho)
    using = Alias de la base de datos
    origin = el origen de la accion
    '''
    try:
        print('Execution started')
        
        #Get inventory instance
        inventoryInstance = Inventory.objects.get(id=instance.inventory_code_id)
        print(f'Old stock:{inventoryInstance.available_quantity}')
        print(f'Stock2Add:{instance.quantity}')
        
        #Update the available quantity
        inventoryInstance.available_quantity += instance.quantity
        print(f'Stock updated:{inventoryInstance.available_quantity}')
        
        inventoryInstance.save()
        print('Saving update...')
        
        #Create inventoryMovement record
        createMovementRecord(instance,1,f'Eliminacion de consumo(Orden #{instance.service_order_id})')
        
    except Exception as e:
        print(f'ERROR({type(e).__name__}):{e}')
    print('END: *** Signal execution #003(ServiceOrder Consumption rollback) ***')
    