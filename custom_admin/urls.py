from . import views
from django.urls import path


urlpatterns = [
    path('', views.admin, name='admin'),
    path('users/', views.user_admin, name='user_admin'),
    path('users/change_admin_status/<str:username>/', views.change_admin_status, name='change_admin_status'),
    path('users/change_membership_status/<str:username>/<str:is_active>/', views.change_membership_status, name='change_membership_status'),
] 