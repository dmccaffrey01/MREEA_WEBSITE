from . import views
from django.urls import path


urlpatterns = [
    path('view/<str:sku>', views.view_notification, name='view_notification'),
    path('visit_url_notification/<str:sku>', views.visit_url_notification, name='visit_url_notification'),
    path('clear_notification/<str:sku>/', views.clear_notification, name='clear_notification'),
    path('unclear_notification/<str:sku>/', views.unclear_notification, name='unclear_notification'),
    path('clear_all_notifications/<str:username>/', views.clear_all_notifications, name='clear_all_notifications'),
    path('unclear_all_notifications/<str:username>/', views.unclear_all_notifications, name='unclear_all_notifications'),
    path('delete_notification/<str:sku>/', views.delete_notification, name='delete_notification'),
    path('delete_notification_from_view/<str:sku>/', views.delete_notification_from_view, name='delete_notification_from_view'),
    path('delete_all_notifications/<str:username>/', views.delete_all_notifications, name='delete_all_notifications'),
    path('get_messages/', views.get_messages, name='get_messages'),
]