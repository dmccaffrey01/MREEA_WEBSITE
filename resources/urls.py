from . import views
from django.urls import path


urlpatterns = [
    path('', views.resources, name='resources'),
    path('<str:folder_name>/', views.folder, name='folder'),
]