from . import views
from django.urls import path


urlpatterns = [
    path('', views.announcements, name='announcements'),
    path('add/', views.add_announcement, name='add_announcement'),
    path('edit/<str:announcement_name>/', views.edit_announcement, name='edit_announcement'),
    path('delete/<str:announcement_name>/', views.delete_announcement, name='delete_announcement'),
]