"""dj_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from allauth.account.views import SignupView
from profiles.forms import CustomSignupForm


app_name = 'account'

urlpatterns = [
    path('default_admin/', admin.site.urls),
    path('', include('home.urls')),
    path('events/', include('events.urls')),
    path('resources/', include('resources.urls')),
    path('members/', include('members.urls')),
    path('contact/', include('contact.urls')),
    path('profile/', include('profiles.urls')),
    path('admin/', include('custom_admin.urls')),
    path('membership/', include('membership.urls')),
    path('accounts/signup/', SignupView.as_view(form_class=CustomSignupForm, success_url='/membership/redirect'), name='account_signup'),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
