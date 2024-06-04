from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='home'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('testimonials/add/<str:username>', views.add_testimonial, name='add_testimonial'),
    path('testimonials/edit/<str:username>', views.edit_testimonial, name='edit_testimonial'),
]