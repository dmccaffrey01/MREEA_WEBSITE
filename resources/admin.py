from django.contrib import admin
from .models import Resource, ResourceType, Folder


class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name_plural = 'Categories'

    list_display = ('friendly_name', 'name',)


class ClassAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name_plural = 'Classes'

    list_display = ('friendly_name', 'name',)


admin.site.register(Resource)
admin.site.register(ResourceType)
admin.site.register(Folder)
