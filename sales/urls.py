from django.urls import path

from . import views

urlpatterns = [
    path('', views.sales_list_view, name='sales_list'),
    path('create', views.sale_add_view, name='add_sale')
]