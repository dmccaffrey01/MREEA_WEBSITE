from . import views
from django.urls import path


urlpatterns = [
    path('', views.members, name='members'),
    path('get_member_classes/<str:username>/', views.get_member_classes, name='get_member_classes'),
    path('management/', views.members_management, name='members_management'),
    path('management/change_admin_status/<str:username>/', views.change_admin_status, name='change_admin_status'),
    path('management/change_membership_status/<str:username>/<str:is_active>/', views.change_membership_status, name='change_membership_status'),
]