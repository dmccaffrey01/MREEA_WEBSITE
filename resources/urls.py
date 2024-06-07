from . import views
from django.urls import path


urlpatterns = [
    path('', views.resources, name='resources'),
    path('<str:folder_name>/', views.folder, name='folder'),
    path('deleted/folders/', views.deleted_folders, name='deleted_folders'),
    path('<str:folder_name>/add/resource/', views.add_resource, name='add_resource'),
    path('<str:folder_name>/edit/resource/<str:resource_name>/', views.edit_resource, name='edit_resource'),
    path('<str:folder_name>/delete/resource/<str:resource_name>/', views.delete_resource, name='delete_resource'),
    path('<str:folder_name>/add/folder/', views.add_folder, name='add_folder'),
    path('<str:folder_name>/edit/folder/<str:selected_folder_name>/', views.edit_folder, name='edit_folder'),
    path('<str:folder_name>/delete/folder/<str:selected_folder_name>/', views.delete_folder, name='delete_folder'),
    path('restore/folder/<str:selected_folder_name>/', views.restore_folder, name='restore_folder'),
]