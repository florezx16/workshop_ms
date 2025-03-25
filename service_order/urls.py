from django.urls import path
from . import views

app_name = 'service_orders'
urlpatterns = [
    path(route='list/',view=views.ServiceOrder_ListView.as_view(),name='grid'),
    path(route='create/',view=views.ServiceOrder_CreateView.as_view(),name='create'),
    path(route='detail/<int:pk>',view=views.ServiceOrder_DetailView.as_view(),name='detail'),
    path(route='delete/<int:serviceOrder_id>',view=views.ServiceOrder_DeleteView.as_view(),name='delete'),
    path(route='flowUpdate/<int:pk>',view=views.ServiceOrder_UpdateView.as_view(),name='flowUpdate'),
    path(route='report/<int:pk>',view=views.ServiceOrder_ReportView.as_view(),name='report'),
    path(route='cancelOrder/<int:pk>',view=views.serviceOrder_Cancel.as_view(),name='cancel'),
    path(route='consumptionPanel/<int:serviceOrder_id>',view=views.ServiceOrderConsumption_ListView.as_view(),name='consumptionPanel'),
    path(route='AddConsumption/<int:serviceOrder_id>',view=views.ServiceOrderConsumption_CreateView.as_view(),name='AddConsumption'),
    path(route='DeleteConsumption/<int:pk>',view=views.ServiceOrderConsumtion_delete.as_view(),name='DeleteConsumption'),
]
