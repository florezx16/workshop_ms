from django.urls import path
from . import views

app_name = 'inventory'
urlpatterns = [
    path(route='grid-code/', view=views.InventoryCodesListView.as_view(), name='grid_code'),
    path(route='create-code/', view=views.InventoryCodesCreateView.as_view(), name='create_code'),
    path(route='update-code/<int:pk>', view=views.InventoryCodesUpdateView.as_view(), name='update_code'),
    path(route='delete-code/<int:pk>', view=views.InventoryCodesDeleteView.as_view(), name='delete_code'),
    path(route='grid/',view=views.InventoryListView.as_view(),name='grid'),
    path(route='create/',view=views.InventoryCreateView.as_view(),name='create'),
    path(route='delete/<int:pk>',view=views.InventoryDeleteView.as_view(),name='delete'), 
    path(route='inventory_in/<int:inventory_code>',view=views.InventoryMovements_CreateView.as_view(),name='inventory_in'),
    path(route='movements_grid/',view=views.InventoryMovement_ListView.as_view(),name='movements_grid'),
    path(route='movement_detail/<int:pk>',view=views.InventoryMovement_DetailView.as_view(),name='movement_detail'),
]