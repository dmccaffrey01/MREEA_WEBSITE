from . import views
from django.urls import path


urlpatterns = [
    path('', views.members, name='members'),
    path('get_member_classes/<str:username>/', views.get_member_classes, name='get_member_classes'),
]