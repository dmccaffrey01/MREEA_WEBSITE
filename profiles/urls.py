from . import views
from django.urls import path


urlpatterns = [
    path('login_redirect/', views.login_redirect, name='login_redirect'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('<str:username>/edit/picture', views.edit_profile_picture, name='edit_profile_picture'),
]