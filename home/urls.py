from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='home'),
    path('testimonials/', views.testimonials, name='testimonials'),
]