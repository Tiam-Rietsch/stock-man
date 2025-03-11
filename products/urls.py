from django.urls import path 

from . import views

urlpatterns = [
    path('', views.products_list_view, name='products_list'),
]