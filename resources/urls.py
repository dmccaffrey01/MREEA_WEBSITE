from . import views
from django.urls import path


urlpatterns = [
    path('', views.all_resources, name='all_resources'),
    path('quick/', views.quick_resources, name='quick_resources'),
    path('<str:folder_name>/', views.folder, name='folder'),
]