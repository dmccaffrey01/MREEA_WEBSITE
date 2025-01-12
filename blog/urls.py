from . import views
from django.urls import path


urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    # path('<str:slug>/view', views.blog_detail, name='blog_detail'),
    # path('add/', views.add_blog, name='add_blog'),
]