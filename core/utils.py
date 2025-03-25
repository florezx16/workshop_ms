from django.db.models import Q
from inventory.models import Inventory,InventoryMovement

def PrepareFilters(data,filters_dict):
    query_filters = Q()
    for k,v in data.items():
        if v:
            filter_spec = filters_dict.get(k)
            if isinstance(filter_spec,list):#Check if filter_spec has a list or not 
                field_name, filter_type = filter_spec[0], filter_spec[1] #Assign the values
            else:
                field_name, filter_type = k, filter_spec
            query_condition = f'{field_name}__{filter_type}' #Prepare query conditions based on filter_spec
            query_filters &= Q(**{query_condition:v}) #Send as argument the query condition(dict)
    query_filters &= Q(status = 1)
    return query_filters

def createMovementRecord(instance,movementType,movementDescription):
    print('Adding InventoryMovement record')
    print(f'Type: {movementType}')
    print(f'Description: {movementDescription}')
    try:
        inventoryInstance = Inventory.objects.get(id=instance.inventory_code_id)
        
        #Save inventoryMovement record
        InventoryMovement.objects.create(
            inventory_code = inventoryInstance,
            type = movementType,
            quantity = instance.quantity,
            description = movementDescription
        )
    except Inventory.DoesNotExist:
        print('ERROR: Inventory instance not found.')
    except Exception as e:
        print(f'ERROR({type(e).__name__}):{e}')
        
