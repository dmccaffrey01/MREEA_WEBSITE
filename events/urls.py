from . import views
from django.urls import path


urlpatterns = [
    path('', views.events, name='events'),
    path('event/<str:event_id>', views.event_detail, name='event_detail'),
]