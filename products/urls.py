from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_list_view, name='products_list'),
    path('create/', views.product_add_view, name='add_product'),
    path('edit/<uuid:id>/', views.product_edit_view, name='edit_product'),
    path('delete/<uuid:id>/', views.product_delete_view, name='delete_product'),

]