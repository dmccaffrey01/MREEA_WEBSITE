from . import views
from django.urls import path


urlpatterns = [
    path('members/', views.member_management, name='member_management'),
]