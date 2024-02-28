from . import views
from django.urls import path


urlpatterns = [
    path('redirect/', views.membership_redirect, name='membership_redirect'),
    path('redirect/success', views.membership_redirect_success, name='membership_redirect_success'),
    path('status/', views.membership_status, name='membership_status'),
    path('', views.membership_status, name='membership'),
    path('cancel/', views.membership_cancel, name='membership_cancel'),
]