from . import views
from django.urls import path


urlpatterns = [
    path('', views.events, name='events'),
    path('add/', views.add_event, name='add_event'),
    path('edit/<str:event_name>/', views.edit_event, name='edit_event'),
]