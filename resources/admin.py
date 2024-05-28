from django.contrib import admin
from .models import Resource, Folder, Icon


admin.site.register(Resource)
admin.site.register(Icon)
admin.site.register(Folder)
