from django.contrib import admin
from .models import Resource, Folder, ResourceType


admin.site.register(Resource)
admin.site.register(ResourceType)
admin.site.register(Folder)
