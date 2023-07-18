from django.contrib import admin

from .models import User, Event, MemberProfile

admin.site.register(User)
admin.site.register(Event)
admin.site.register(MemberProfile)