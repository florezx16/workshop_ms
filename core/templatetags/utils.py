from django import template

register = template.Library()

@register.filter(name='setValidationClass')
def setValidationClass(input):
    bootstrap_class = ''
    if input.help_text == 'filter_option':
        if input.errors:
            #CSS Class for only filters forms
            bootstrap_class = 'is-invalid'
    else:
        #CSS Class for others forms
        #print(input.widget_type) #Get the widget from the field
        if (input.data != None) and (input.data != []) :
            if input.errors:
                bootstrap_class = 'is-invalid'
            else:
                bootstrap_class = 'is-valid'   
    return input.as_widget(attrs={'class':'form-control '+ bootstrap_class})

@register.filter(name='assetTypeColor')
def assetTypeColor(assetType):
    if assetType == 1:
        return 'primary'
    else:
        return 'warning'

@register.filter(name='flowStatus_mapping')
def ServiceOrder_FlowStatus_Mapping(flowStatus):
    css_class = 'light'
    match flowStatus:
        case 1:#pendingDiagnose
            css_class = 'warning'
            
        case 2:#onRepair
            css_class = 'primary'
            
        case 3:#complete
            css_class = 'success'
            
        case 4:#cancel
            css_class = 'danger'
    return css_class

@register.filter(name='movementType_mapping')
def inventoryMovement_TypeMapping(flowStatus):
    css_class = ''
    match flowStatus:
        case 1:#In
            css_class = 'success'
            
        case 2:#Out
            css_class = 'danger'
    return css_class

@register.simple_tag(takes_context=True)
def querystring_without_page(context):
    request = context['request']
    querydict = request.GET.copy()
    querydict.pop('page',None)
    
    #Delete keys empty or duplicated
    clean_querydict = {k: v for k, v in querydict.items() if v.strip() != ''}
    
    return '&'.join([f'{k}={v}' for k,v in clean_querydict.items()])
