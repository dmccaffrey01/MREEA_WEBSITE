from . import views
from django.urls import path
from allauth.account import views as account_views


urlpatterns = [
    path('', views.index, name='home'),
    path('accounts/signup/', views.signup_view, name='account_signup'),
    path('accounts/login/', account_views.LoginView.as_view(), name='account_login'),
    path('membership/', views.membership, name='membership'),
    path('announcements/', views.announcements, name='announcements'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<str:unique_event_id>/', views.event_detail, name='event_detail'),
    path('events/<str:unique_event_id>/edit/', views.edit_event, name='edit_event'),
    path('get_event_data/', views.get_event_data, name='get_event_data'),
]