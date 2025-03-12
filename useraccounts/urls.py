from django.urls import path 

from . import views 

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.user_list_view, name='user_list'),
    path('users/activate/<uuid:id>/', views.toggle_activate_user, name='toggle_activate_user'),
    path('users/delete/<uuid:id>/', views.delete_user_view, name='delete_user'),
]