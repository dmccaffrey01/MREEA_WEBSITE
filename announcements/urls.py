from . import views
from django.urls import path


urlpatterns = [
    path('', views.announcements, name='announcements'),
    path('<str:announcement_name>/', views.announcement_detail, name='announcement_detail'),
]