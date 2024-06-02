from . import views
from django.urls import path


urlpatterns = [
    path('view/<str:sku>', views.view_notification, name='view_notification'),
    path('clear_all_notifications/<str:username>/', views.clear_all_notifications, name='clear_all_notifications'),
    path('delete_notification_from_view/<str:sku>/', views.delete_notification_from_view, name='delete_notification_from_view'),
    path('delete_all_notifications/<str:username>/', views.delete_all_notifications, name='delete_all_notifications'),
]