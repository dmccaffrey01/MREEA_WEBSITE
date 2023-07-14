from . import views
from django.urls import path
from allauth.account import views as account_views


urlpatterns = [
    path('', views.index, name='home'),
    path('accounts/signup/', views.signup_view, name='account_signup'),
    path('accounts/login/', account_views.LoginView.as_view(), name='account_login'),
    path('membership/', views.membership, name='membership'),
]