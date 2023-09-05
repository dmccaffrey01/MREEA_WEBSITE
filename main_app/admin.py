from django.contrib import admin

from .models import User, Event, MemberProfile, Resource, ResourceCategory, ResourceLinkType, ResourceSubCategory, AspectRatio, ImageSelect

admin.site.register(User)
admin.site.register(Event)
admin.site.register(MemberProfile)
admin.site.register(Resource)
admin.site.register(ResourceCategory)
admin.site.register(ResourceSubCategory)
admin.site.register(ResourceLinkType)
admin.site.register(AspectRatio)
admin.site.register(ImageSelect)