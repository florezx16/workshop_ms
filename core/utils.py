from django.db.models import Q
from django.utils.timezone import make_aware
from inventory.models import Inventory,InventoryMovement
from service_order.models import ServiceOrder, ServiceOrderImages

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

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
    print(f'\tType: {movementType}')
    print(f'\tDescription: {movementDescription}')
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
        
def modifyConsumablesTotal(serviceConsume_obj,acumType):
    print('Update consumables_total')
    try:
        serviceOrder = ServiceOrder.objects.get(id=serviceConsume_obj.service_order_id)
    except ServiceOrder.DoesNotExist:
        print('\tService order instance not found.')
    except Exception as e:
        print(f'ERROR({type(e).__name__}):{e}')
    else:
        print(f'\tacumType:{acumType}')
        print(f'\tServiceOrder instance(ID):{serviceOrder}')
        print(f'\tOld consumables_total:{serviceOrder.consumables_total}')
        print(f'\tPrice2{acumType}:{serviceConsume_obj.total}')
        if acumType=='add':
            serviceOrder.consumables_total += serviceConsume_obj.total
        else:
            serviceOrder.consumables_total -= serviceConsume_obj.total
        print(f'\tNew consumables_total:{serviceOrder.consumables_total}')
        print('\tSaving ServiceOrder changes...')
        serviceOrder.save()
        
def generateDates(currentDate):
    months2reduce = 3 #Months for calculate the differents dates
    datesVault = []
    for i in range(months2reduce):
        dateObject = currentDate - relativedelta(months=i)
        startDate = dateObject + relativedelta(day=1)
        endDate = dateObject + relativedelta(day=31)
        month_name = dateObject.strftime("%B")
        dataDict = {
            'month_name':month_name,
            'dates':{
                'start_date':startDate,
                'end_date':endDate,
            }
        }
        datesVault.append(dataDict)
    return datesVault
    
def pieChart_widgetData():
    #Current time with time zone
    current_time = make_aware(datetime.now())
    
    #3months before - current_data 
    query_time = current_time - timedelta(days=90)
    
    #Execute query
    query = ServiceOrder.objects.filter(status=1,flowStatus__in=[1,2],createtime__range=(query_time,current_time))
    
    pending2diagnose = 0
    pending2repair = 0
    
    #Loop query result
    for serviceOrder in query:
        match serviceOrder.flowStatus:
            case 1:
                pending2diagnose+=1
            case 2:
                pending2repair+=1
    
    #Return as list
    return [pending2diagnose,pending2repair]


def barChart_widgetData():
    #Current time with time zone
    current_time = datetime.now()
    
    #Get dates to query the date
    datesVault = generateDates(current_time)
    
    #Query serviceOrders information according to the dates generated
    months = {}
    totalCompleted = []
    totalCanceled = []
    acum = 1
    for date in datesVault:
        datesValues = date.get('dates')
        count_result = []
        for i in [3,4]:#FlowStatus loop
            startDate = make_aware(datesValues.get('start_date'))
            endDate = make_aware(datesValues.get('end_date'))
            queryCount = ServiceOrder.objects.filter(status=1,flowStatus=i,createtime__range=(startDate,endDate)).count()
            count_result.append(queryCount)
        months[f'month{acum}'] = date.get('month_name')
        totalCompleted.append(count_result[0])
        totalCanceled.append(count_result[1])
        acum+=1

    return {
        'monthsInfo':months,
        'totalCompleted':totalCompleted,
        'totalCanceled':totalCanceled
    }

def getLastInventoryMovements():
    query = InventoryMovement.objects.filter(status=1)[:5]
    return query

def getOrderImagesByFlowStatus(flowStatus,serviceOrderInstance):
    queryResult = ServiceOrderImages.objects.filter(service_order=serviceOrderInstance,flowStatus_related=flowStatus,status=1)
    return queryResult

    