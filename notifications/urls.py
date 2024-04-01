from . import views
from django.urls import path


urlpatterns = [
    path('mark_notificaiton_as_read/<str:sku>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    
]