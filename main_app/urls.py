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
    path('events/<str:event_short_uuid>/', views.event_detail, name='event_detail'),
    path('events/<str:event_short_uuid>/edit/', views.edit_event, name='edit_event'),
    path('get_event_data/', views.get_event_data, name='get_event_data'),
    path('members/', views.members, name='members'),
    path('profile/<str:member_short_uuid>/', views.member_profile, name='member_profile'),
    path('profile/<str:member_short_uuid>/edit', views.edit_member_profile, name='edit_member_profile'),
    path('profile/<str:member_short_uuid>/edit_profile_picture', views.edit_profile_picture, name='edit_profile_picture'),
    path('learn/', views.learn_page, name='learn'),
    path('contact/', views.contact_page, name='contact'),
    path('accounts/password/change/', views.CustomPasswordChangeView.as_view(), name='account_change_password'),
    path('learn/resources', views.resources_page, name='resources'),
    path('learn/resources/add', views.add_resource, name='add_resource'),
    path('learn/resources/edit', views.add_resource, name='edit_resource'),
]