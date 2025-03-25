from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView, TemplateView
from django.template.loader import render_to_string
from .models import Asset
from .forms import AssetMainForm, AssetFilterForm
from core.utils import PrepareFilters

# Create your views here.
class AssetListView(ListView):
    model = Asset
    template_name = "assets/assets_grid.html"
    context_object_name = 'assets'
    paginate_by = 10
    extra_context = {
        'AssetFilterForm':AssetFilterForm
    }
    
    def get_queryset(self):
        if self.request.GET:
            filter_form = AssetFilterForm(self.request.GET)
            if filter_form.is_valid():
                #Prepare filters dict
                filters_dict = {
                    'name':'icontains',
                    'document_id':'exact',
                    'type':'exact'
                }
                query_filters = PrepareFilters(filter_form.cleaned_data,filters_dict)
                queryset = Asset.objects.filter(query_filters)
                return queryset
            else:
                messages.error(request=self.request,message='Tus filtros presentan algunas inconsistencias, por favor revisalos e intentalo nuevamente.')
        
        #No GET request
        queryset = Asset.objects.filter(status = 1)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['AssetFilterForm'] = AssetFilterForm(self.request.GET)
        context['active_link'] = 'assets'
        return context

class AssetCreateView(CreateView):
    model = Asset
    form_class = AssetMainForm
    template_name = "assets/assets_create.html"
    success_url = reverse_lazy('assets:grid')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_link'] = 'assets'
        return context
    
    def form_valid(self,form):
        if self.request.GET.get('popup') == '1':
            #form.instance.type - Get current form values 
            self.object = form.save()#Save the object
            return JsonResponse({
                'status':True,
                'last_record':self.object.id
            })
        else:
            messages.success(request=self.request,message='El Asset se ha creado de manera exitosa.')
            return super().form_valid(form)

    def form_invalid(self,form):
        messages.error(request=self.request,message='El formulario presenta algunos errores, por favor verificarlos e intentalo nuevamente.')
        return super().form_invalid(form)
            
class AssetUpdateView(UpdateView):
    model = Asset
    template_name = "assets/assets_update.html"
    form_class = AssetMainForm
    context_object_name = 'asset'
    success_url = reverse_lazy('assets:grid')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_link'] = 'assets'
        return context
    
    def form_valid(self, form: AssetMainForm):
        messages.success(request=self.request,message='El Asset se ha modificado de manera exitosa.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(request=self.request,message='El formulario presenta algunos errores, por favor verificarlos e intentarlo nuevamente.')
        return super().form_invalid(form)
    
class AssetDeleteView(TemplateView):
    template_name = 'assets/assets_delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asset = get_object_or_404(Asset,id=self.kwargs['asset_id'])
        context['asset'] = asset
        context['active_link'] = 'assets'
        return context
    
    def post(self, request, *args, **kwargs):
        asset = get_object_or_404(Asset,id=self.kwargs['asset_id'])
        asset.status = 0
        asset.save()
        messages.success(request=self.request,message='El Asset se ha deshabilitado de manera exitosa.')
        return redirect(reverse_lazy('assets:grid'))

def updateSelect_load(request):
    assetsOptions = Asset.objects.filter(status=1,type=1).values('id','name')
    return JsonResponse({
        'result':True,
        'assetsOptions':list(assetsOptions)
    })
    