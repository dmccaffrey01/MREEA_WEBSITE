from . import views
from django.urls import path


urlpatterns = [
    path('', views.notifications, name='notifications'),
    path('clear_notification/<str:sku>/', views.clear_notification, name='clear_notification'),
    path('delete_notification/<str:sku>/', views.delete_notification, name='delete_notification'),
    path('get_messages/', views.get_messages, name='get_messages'),
]