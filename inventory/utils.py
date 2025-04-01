from datetime import datetime

def get_inventory_imagePath(instance,filename):
    currentDate = datetime.now()
    timestamp = currentDate.strftime("%Y%m%d%H%M%S%f")
    fileExt = filename[filename.index('.'):]
    newFileName = f'{timestamp}{fileExt}'
    path = f'inventory/{instance.code}/{newFileName}'
    return path