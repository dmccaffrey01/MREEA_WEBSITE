from django.contrib import admin

from .models import User, Event, MemberProfile, Resource, ResourceCategory, ResourceLinkType

admin.site.register(User)
admin.site.register(Event)
admin.site.register(MemberProfile)
admin.site.register(Resource)
admin.site.register(ResourceCategory)
admin.site.register(ResourceLinkType)