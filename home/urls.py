from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='home'),
    path('privacy/', views.privacy, name='privacy'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('testimonials/add/<str:username>', views.add_testimonial, name='add_testimonial'),
    path('testimonials/edit/<str:username>', views.edit_testimonial, name='edit_testimonial'),
    path('testimonials/approve/<str:testimonial_id>', views.approve_testimonial, name='approve_testimonial'),
    path('testimonials/deny/<str:testimonial_id>', views.deny_testimonial, name='deny_testimonial'),
]