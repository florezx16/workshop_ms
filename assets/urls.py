from django.urls import path
from .views import AssetCreateView,AssetListView,AssetUpdateView,AssetDeleteView,updateSelect_load

app_name = 'assets'
urlpatterns = [
    path(route='grid/',view=AssetListView.as_view(),name='grid'),
    path(route='create/',view=AssetCreateView.as_view(),name='create'),
    path(route='update/<int:pk>',view=AssetUpdateView.as_view(),name='update'),
    path(route='delete/<int:asset_id>',view=AssetDeleteView.as_view(),name='delete'),
    path(route='updateSelect/',view=updateSelect_load,name='updateSelect')
]

