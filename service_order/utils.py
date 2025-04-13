from datetime import datetime
            
def SetNextFlowStatus(currentStatus):
    nextStatus = currentStatus
    match currentStatus:
        case 1:#pendingDiagnose    
            nextStatus = 2 #onRepair
            
        case 2:#onRepair    
            nextStatus = 3 #complete
            
    return nextStatus            

def MappingFlowStatus(serviceOrder):
    flowStatus = serviceOrder.flowStatus
    match flowStatus:
        case 1:
            return 'pendingDiagnose'
        case 2:
            return 'onRepair'
        case 3:
            return 'complete'
        case _:
            return 'default'
    
def get_serviceOrder_imagePath(instance,filename):
    currentDate = datetime.now()
    timestamp = currentDate.strftime("%Y%m%d%H%M%S%f")
    fileExt = filename[filename.index('.'):]
    newFileName = f'{timestamp}{fileExt}'
    flowStatus = MappingFlowStatus(instance.service_order)
    path = f'service_order/{instance.service_order.id}/{flowStatus}/{newFileName}'
    return path

 

    