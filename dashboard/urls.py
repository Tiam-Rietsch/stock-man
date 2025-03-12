from django.urls import path 

from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('api/dashboard-data/', views.get_chart_data, name='dashboard_data'),
]