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
from profiles.views import CustomPasswordChangeView


app_name = 'account'

urlpatterns = [
    path('default_admin/', admin.site.urls),
    path('', include('home.urls')),
    path('events/', include('events.urls')),
    path('resources/', include('resources.urls')),
    path('members/', include('members.urls')),
    path('contact/', include('contact.urls')),
    path('profile/', include('profiles.urls')),
    path('membership/', include('membership.urls')),
    path('announcements/', include('announcements.urls')),
    path('blog/', include('blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('notifications/', include('notifications.urls')),
    path('accounts/password/change/', CustomPasswordChangeView.as_view(), name='account_change_password'),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
