from . import views
from django.urls import path


urlpatterns = [
    path('', views.admin, name='admin'),
    path('users/', views.user_admin, name='user_admin'),
] 