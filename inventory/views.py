from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DetailView
from .models import Inventory, InventoryCodes, InventoryMovement
from .forms import InventoryCodeMainForm, InventoryCodeFilterForm, InventoryMainForm, InventoryFilterForm, InventoryMovement_MainForm, InventoryMovement_FilterForm
from core.utils import PrepareFilters

# Create your views here.
class InventoryCodesListView(ListView):
    model = InventoryCodes
    template_name = "inventory/code_grid.html"
    context_object_name = 'codes'
    paginate_by = 10
    extra_context = {
        'CodeFilterForm':InventoryCodeFilterForm
    }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['CodeFilterForm'] = InventoryCodeFilterForm(self.request.GET)
        context['active_link'] = 'code_mngt'
        context['dropdown_menu'] = True
        return context
    
    def get_queryset(self):
        if self.request.GET:
            filter_form = InventoryCodeFilterForm(self.request.GET)
            if filter_form.is_valid():
                #Prepare filters dict
                filters_dict = {
                    'code':'iexact',
                    'name':'icontains',
                    'supplier':'exact'
                }
                query_filters = PrepareFilters(filter_form.cleaned_data,filters_dict)
                queryset = InventoryCodes.objects.filter(query_filters)
                return queryset
            else:
                messages.error(request=self.request,message='Tus filtros presentan algunas inconsistencias, por favor revisalos e intentalo nuevamente.')
            
        #No GET request
        queryset = InventoryCodes.objects.filter(status = 1)
        return queryset
    
class InventoryCodesCreateView(CreateView):
    model = InventoryCodes
    form_class = InventoryCodeMainForm
    template_name = "inventory/code_create.html"
    success_url = reverse_lazy('inventory:grid_code')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_link'] = 'code_mngt'
        context['dropdown_menu'] = True
        return context

    def form_valid(self, form):
        messages.success(request=self.request,message='El código se ha añadido de manera exitosa al listado.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(request=self.request,message='El formulario presenta algunos errores, por favor verificarlos e intentalo nuevamente.')
        return super().form_invalid(form)
    
class InventoryCodesUpdateView(UpdateView):
    model = InventoryCodes
    template_name = "inventory/code_update.html"
    form_class = InventoryCodeMainForm
    context_object_name = 'code'
    success_url = reverse_lazy('inventory:grid_code')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_link'] = 'code_mngt'
        context['dropdown_menu'] = True
        return context
    
    def form_valid(self, form):
        messages.success(request=self.request,message='El código se ha modificado de manera exitosa.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(request=self.request,message='El formulario presenta algunos errores, por favor verificarlos e intentarlo nuevamente.')
        return super().form_invalid(form)
    
class InventoryCodesDeleteView(TemplateView):
    template_name = 'inventory/code_delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        code = get_object_or_404(InventoryCodes,id=self.kwargs['pk'])
        context['active_link'] = 'code_mngt'
        context['dropdown_menu'] = True
        context['code'] = code
        return context
    
    def post(self, request, *args, **kwargs):
        code = get_object_or_404(InventoryCodes,id=self.kwargs['pk'])
        code.status = 0
        code.save()
        messages.success(request=self.request,message='El código se ha deshabilitado de manera exitosa.')
        return redirect(reverse_lazy('inventory:grid_code'))

class InventoryListView(ListView):
    model = Inventory
    template_name = "inventory/inventory_grid.html"
    context_object_name = 'inventory'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['InventoryFilterForm'] = InventoryFilterForm(self.request.GET)
        context['active_link'] = 'inventory'
        context['dropdown_menu'] = True
        return context
    
    def get_queryset(self):
        if self.request.GET:
            filter_form = InventoryFilterForm(self.request.GET)
            if filter_form.is_valid():
                #Prepare filters dict
                filters_dict = {
                    'code':['code__code','exact']
                }
                query_filters = PrepareFilters(filter_form.cleaned_data,filters_dict)                
                queryset = Inventory.objects.filter(query_filters)
                return queryset
            else:
                messages.error(request=self.request,message='Tus filtros presentan algunas inconsistencias, por favor revisalos e intentalo nuevamente.')
            
        #No GET request
        queryset = Inventory.objects.filter(status = 1)
        return queryset

class InventoryCreateView(CreateView):
    model = Inventory
    form_class = InventoryMainForm
    template_name = "inventory/inventory_create.html"
    success_url = reverse_lazy('inventory:grid')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_link'] = 'inventory'
        context['dropdown_menu'] = True
        return context

    def form_valid(self, form):
        messages.success(request=self.request,message='')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(request=self.request,message='El formulario presenta algunos errores, por favor verificarlos e intentalo nuevamente.')
        return super().form_invalid(form)
    
class InventoryUpdateView(UpdateView):
    model = Inventory
    template_name = "inventory/inventory_update.html"
    form_class = InventoryMainForm
    context_object_name = 'inventory_item'
    success_url = reverse_lazy('inventory:grid')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_link'] = 'inventory'
        context['dropdown_menu'] = True
        return context
    
    def form_valid(self, form):
        messages.success(request=self.request,message='El inventario ha sido modificado de manera existosa.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(request=self.request,message='El formulario presenta algunos errores, por favor verificarlos e intentarlo nuevamente.')
        return super().form_invalid(form)
    
class InventoryDeleteView(TemplateView):
    template_name = 'inventory/inventory_delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        code = get_object_or_404(Inventory,id=self.kwargs['pk'])
        context['code'] = code
        context['active_link'] = 'inventory'
        context['dropdown_menu'] = True
        return context
    
    def post(self, request, *args, **kwargs):
        item = get_object_or_404(Inventory,id=self.kwargs['pk'])
        item.status = 0
        item.save()
        messages.success(request=self.request,message='El item en del inventario se ha deshabilitado de manera exitosa.')
        return redirect(reverse_lazy('inventory:grid'))
    
class InventoryMovements_CreateView(CreateView):
    model = InventoryMovement
    form_class = InventoryMovement_MainForm
    template_name = "inventory/inventoryMovement_create.html"
    success_url = reverse_lazy('inventory:grid')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_link'] = 'inventory'
        context['dropdown_menu'] = True
        context['inventory_instance'] = get_object_or_404(Inventory.objects.filter(status=1),id=self.kwargs.get('inventory_code'))
        return context

    def form_valid(self, form):
        messages.success(request=self.request,message='La existencia se ha añadido de manera existosa.')
        inventoryInstance = get_object_or_404(Inventory.objects.filter(status=1),id=self.kwargs.get('inventory_code'))
        
        #Pre-save object
        self.object = form.save(commit=False)
        self.object.inventory_code = inventoryInstance#self.kwargs.get('inventory_code')
        self.object.type = 1 #In
        self.object.is_inbound = True #Inbound flag
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(request=self.request,message='El formulario presenta algunos errores, por favor verificarlos e intentalo nuevamente.')
        return super().form_invalid(form)

class InventoryMovement_ListView(ListView):
    model = InventoryMovement
    template_name = "inventory/inventoryMovement_grid.html"
    context_object_name = 'movements'
    paginate_by = 10
    extra_context = {
        'MovementFilterForm':InventoryMovement_FilterForm
    }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MovementFilterForm'] = InventoryMovement_FilterForm(self.request.GET)
        context['active_link'] = 'inventory_movement'
        context['dropdown_menu'] = True
        return context
    
    def get_queryset(self):
        if self.request.GET:
            filter_form = InventoryMovement_FilterForm(self.request.GET)
            if filter_form.is_valid():
                #Prepare filters dict
                filters_dict = {
                    'inventory_code':'exact',
                    'type':'exact'
                }
                query_filters = PrepareFilters(filter_form.cleaned_data,filters_dict)
                queryset = InventoryMovement.objects.filter(query_filters)
                return queryset
            else:
                messages.error(request=self.request,message='Tus filtros presentan algunas inconsistencias, por favor revisalos e intentalo nuevamente.')
            
        #No GET request
        queryset = InventoryMovement.objects.filter(status = 1)
        return queryset
    
class InventoryMovement_DetailView(DetailView):
    model = InventoryMovement
    context_object_name = 'movement'
    template_name = 'inventory/inventoryMovement_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_link'] = 'inventory_movement'
        context['dropdown_menu'] = True
        return context