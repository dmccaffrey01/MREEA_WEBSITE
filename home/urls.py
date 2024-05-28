from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='home'),
    path('faqs/', views.faqs, name='faqs'),
]