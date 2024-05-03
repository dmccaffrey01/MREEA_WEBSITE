from . import views
from django.urls import path


urlpatterns = [
    path('clear_notification/<str:sku>/', views.clear_notification, name='clear_notification'),
    path('get_messages/', views.get_messages, name='get_messages'),
]