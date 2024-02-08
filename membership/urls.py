from . import views
from django.urls import path


urlpatterns = [
    path('payment/', views.membership_payment, name='membership_payment'),
    path('payment/success', views.membership_payment_success, name='membership_payment_success'),
]