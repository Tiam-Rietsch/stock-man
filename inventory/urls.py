from django.urls import path 

from . import views


urlpatterns = [
    path('inventory/', views.inventory_view, name='inventory'),
    path('update/stock/<uuid:id>/', views.stock_update_view, name='stock_update'),
    path('export-inventory/', views.export_inventory_to_excel, name='export_inventory'), 
]