from django.urls import path
from . import views

urlpatterns = [
    path('', views.contentAdmin, name='contentAdmin'),
    path('CRMAdmin/', views.CRMAdmin, name='CRMAdmin'),
]