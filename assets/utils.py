from django.db.models import Q

def prepare_Asset_queryFilters(query_data):
    query_filters = Q()#Define main Q() object
    for k,v in query_data.items():
        if v:
            #Prepare Q() object based on dict key
            match k:
            #Build Q() object
                case 'name':
                    query_filters &= Q(name__icontains = v)
                case 'document_id':
                    query_filters &= Q(document_id = v)
                case 'type':
                    query_filters &= Q(type = v)
    
    #Final Q() object 
    query_filters &= Q(status = 1)
    return query_filters
    