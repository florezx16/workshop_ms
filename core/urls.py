from django.urls import path
from . import views

core_urlpatterns = ([
    path(route='',view=views.index,name='index')
],'core')
