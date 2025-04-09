from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, TemplateView, DetailView, UpdateView, DeleteView
from django.utils import timezone
from django.db.models import Q
from .models import ServiceOrder, ServiceOrderImages, ServiceOrderConsumption
from .forms import *
from core.utils import PrepareFilters
from .utils import SetNextFlowStatus
from assets.models import Asset
from core.models import CoreInformation

# Create your views here.
class ServiceOrder_ListView(ListView):
    Model = ServiceOrder
    template_name = 'service_order/serviceOrder_grid.html'
    context_object_name = 'service_orders'
    paginate_by = 10
    extra_context = {
        'ServiceOrderFilterForm':ServiceOrderFilterForm
    }
    
    def get_queryset(self):
        if self.request.GET:
            filter_form = ServiceOrderFilterForm(self.request.GET)
            if filter_form.is_valid():
                #Prepare filters dict
                filters_dict = {
                    'customer':'exact',
                    'serial':'iexact',
                    'model':'icontains'
                }
                query_filters = PrepareFilters(filter_form.cleaned_data,filters_dict)
                queryset = ServiceOrder.objects.filter(query_filters)
                return queryset
            else:
                messages.error(request=self.request,message='Tus filtros presentan algunas inconsistencias, por favor revisalos e intentalo nuevamente.')
        
        #No GET request
        queryset = ServiceOrder.objects.filter(status = 1)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ServiceOrderFilterForm'] = ServiceOrderFilterForm(self.request.GET)
        context['active_link'] = 'service_orders'
        return context
    
class ServiceOrder_CreateView(CreateView):
    model = ServiceOrder
    template_name = 'service_order/serviceOrder_create.html'
    form_class = serviceOrders_MainForm
    success_url = reverse_lazy('service_orders:grid')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_link'] = 'service_orders'
        return context
    
    def form_valid(self, form):
        messages.success(request=self.request,message='La orden de servicio de ha registrado de manera correcta.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(request=self.request,message='El formulario presenta algunos errores, por favor verificarlos e intentalo nuevamente.')
        return super().form_invalid(form)
    
class ServiceOrder_DetailView(DetailView):
    model = ServiceOrder
    template_name = 'service_order/serviceOrder_details.html'
    context_object_name = 'serviceOrder '
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_link'] = 'service_orders'
        context['serviceOrder'] = self.object
        return context

class ServiceOrder_DeleteView(TemplateView):
    template_name = 'service_order/serviceOrder_delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_order = get_object_or_404(ServiceOrder,id=self.kwargs['serviceOrder_id'])
        context['serviceOrder'] = service_order
        context['active_link'] = 'service_orders'
        return context
    
    def post(self, request, *args, **kwargs):
        service_order = get_object_or_404(ServiceOrder,id=self.kwargs['serviceOrder_id'])
        service_order.status = 0
        service_order.save()
        messages.success(request=self.request,message='La orden de servicio se ha deshabilitado de manera exitosa.')
        return redirect(reverse_lazy('service_orders:grid'))
    
class ServiceOrder_UpdateView(UpdateView):
    model = ServiceOrder
    template_name = "service_order/serviceOrder_workFlow.html"
    context_object_name = 'service_order'
    success_url = reverse_lazy('service_orders:grid')
    
    def get_form_class(self):
        currentObject = self.get_object()
        form_class = None
        
        #Check flowStatus
        match currentObject.flowStatus:
            case 1:
                form_class = serviceOrders_DiagnoseForm
                
            case 2:
                form_class = serviceOrders_RepairForm
                        
        #Return form based on flowStatus
        return form_class
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_link'] = 'service_orders'
        context['cancel_form'] = serviceOrders_CancelForm
        return context
        
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
        
    #Save the object
    def form_valid(self, form):
        messages.success(request=self.request,message='La orden de servicio se ha actualizado de manera exitosa.')
        currentObject = self.get_object()
        
        #Get all images from the form (Already sanitized)
        images = form.cleaned_data['images']

        #Check if the images has values
        if len(images)>0:
            #Save all the images related to the order
            for image in images:
                try:
                    ServiceOrderImages.objects.create(
                        service_order = currentObject,
                        image = image
                    )
                except Exception as e:
                    raise RuntimeError('Something went wrong while saving the image. Please contact the system administrator.')
            
        #Delete image field from cleanedData dict
        del form.cleaned_data['images']
        
        #Add pre-save instance and add FlowStatus
        self.object = form.save(commit=False)
        self.object.flowStatus = SetNextFlowStatus(currentObject.flowStatus)
        self.object.diagnose_date = timezone.now() if currentObject.flowStatus == 1 else currentObject.diagnose_date
        self.object.repair_date = timezone.now() if currentObject.flowStatus == 2 else currentObject.repair_date
        
        #Save the object
        return super().form_valid(form)
    
    #Return the form with errors
    def form_invalid(self, form):
        messages.error(request=self.request,message='El formulario presenta algunos errores, por favor verificarlos e intentarlo nuevamente.')
        return super().form_invalid(form)
    
class ServiceOrder_ReportView(DetailView):
    model = ServiceOrder
    template_name = 'service_order/serviceOrder_report.html'
    context_object_name = 'serviceOrder'
    
    
    def get_context_data(self, **kwargs):
        #ServiceOrder instance
        serviceOrder = self.get_object()
        
        #Company core information
        core_info = CoreInformation.objects.get(id=1)
        
        #Customer instance
        customer = Asset.objects.get(id=serviceOrder.customer_id)
        
        #Consumption results
        consumblesResults = ServiceOrderConsumption.objects.filter(service_order=serviceOrder.id).order_by('-createtime')
        
        context = super().get_context_data(**kwargs)
        context['active_link'] = 'service_orders'
        context['coreInfo'] = core_info
        context['serviceOrder'] = serviceOrder
        context['customer'] = customer
        context['consumblesResults'] = consumblesResults
        context['serviceOrder_Total'] = serviceOrder.services_total + serviceOrder.consumables_total
        return context
    
class serviceOrder_Cancel(UpdateView):
    model = ServiceOrder
    form_class = serviceOrders_CancelForm
    template_name = "service_order/serviceOrder_cancel.html"
    context_object_name = 'service_order'
    success_url = reverse_lazy('service_orders:grid')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_link'] = 'service_orders'
        context['serviceOrder'] = self.object
        return context
    
    def form_valid(self, form):
        messages.success(request=self.request,message='La orden de servicio se ha cancelado de manera correcta.')
        self.object = form.save(commit=False)
        self.object.flowStatus = 4
        self.object.cancel_date = timezone.now()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(request=self.request,message='El formulario presenta algunos errores, por favor verificarlos e intentarlo nuevamente.')
        return super().form_invalid(form)
    
#CONSUMPTION VIEWS
class ServiceOrderConsumption_ListView(ListView):
    model = ServiceOrderConsumption
    template_name = 'service_order/serviceOrderConsumption_grid.html'
    context_object_name = 'serviceOrders_consumptions'
    paginate_by = 10
    extra_context = {
        'ServiceOrderConsumptionFilterForm':ServiceOrderConsumptionFilterForm
    }
    
    def get_queryset(self):
        if self.request.GET:
            filter_form = ServiceOrderConsumptionFilterForm(self.request.GET)
            if filter_form.is_valid():
                #Prepare filters dict
                filters_dict = {
                    'inventory_code':'exact'
                }
                query_filters = PrepareFilters(filter_form.cleaned_data,filters_dict)
                queryset = ServiceOrderConsumption.objects.filter(query_filters,Q(service_order=self.kwargs.get('serviceOrder_id'))).order_by('-createtime')
                return queryset
            else:
                messages.error(request=self.request,message='Tus filtros presentan algunas inconsistencias, por favor revisalos e intentalo nuevamente.')
        
        #No GET request
        queryset = ServiceOrderConsumption.objects.filter(status=1,service_order=self.kwargs.get('serviceOrder_id')).order_by('-createtime')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ServiceOrderConsumptionFilterForm'] = ServiceOrderConsumptionFilterForm(self.request.GET)
        context['ServiceOrder'] = get_object_or_404(ServiceOrder.objects.filter(flowStatus=3,status=1),pk=self.kwargs.get('serviceOrder_id'))
        context['active_link'] = 'service_orders'
        return context
    
class ServiceOrderConsumption_CreateView(CreateView):
    model = ServiceOrderConsumption
    template_name = 'service_order/serviceOrderConsumption_create.html'
    form_class = ServiceOrderConsumption_MainForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_link'] = 'service_orders'
        context['ServiceOrder'] = get_object_or_404(ServiceOrder.objects.filter(flowStatus=3,status=1),pk=self.kwargs.get('serviceOrder_id'))
        return context
    
    def form_valid(self, form):
        messages.success(request=self.request,message='La orden de servicio de ha registrado de manera correcta.')
        inventory = form.cleaned_data.get('inventory_code')
        quantity = form.cleaned_data.get('quantity')
        
        #pre-Save object
        self.object = form.save(commit=False)
        self.object.service_order = get_object_or_404(ServiceOrder.objects.filter(flowStatus=3,status=1),pk=self.kwargs.get('serviceOrder_id'))
        self.object.unit_price = inventory.code.inbound_price
        self.object.total = (quantity*inventory.code.inbound_price)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(request=self.request,message='El formulario presenta algunos errores, por favor verificarlos e intentalo nuevamente.')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('service_orders:consumptionPanel',args=[self.kwargs.get('serviceOrder_id')])
    
class ServiceOrderConsumtion_delete(DeleteView):
    model = ServiceOrderConsumption
    template_name = 'service_order/serviceOrderConsumption_delete.html'
    context_object_name = 'serviceOrder_consumption'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_link'] = 'service_orders'
        return context
        
    def get_success_url(self):
        messages.success(request=self.request,message='El consumo de la orden se ha eliminado exitosamente.')
        serviceOrder = self.get_object()
        return reverse_lazy('service_orders:consumptionPanel',args=[serviceOrder.service_order.id])
    
class ServiceOrder_serviceConfig(UpdateView):
    model = ServiceOrder
    template_name = "service_order/serviceOrder_servicesConfig.html"
    context_object_name = 'service_order'
    success_url = reverse_lazy('service_orders:grid')
    form_class = serviceOrders_ServiceConfigForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_link'] = 'service_orders'
        return context
    
    def form_valid(self, form):
        messages.success(request=self.request,message='Has actualizado los costos de servicio de manera exitosa.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(request=self.request,message='El formulario presenta algunos errores, por favor verificarlos e intentarlo nuevamente.')
        return super().form_invalid(form)
    
    
    
    