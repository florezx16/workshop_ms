from django.urls import path
from .views import index_TemplateView

app_name = 'core'
urlpatterns = [
    path(route='',view=index_TemplateView.as_view(),name='index')
]
