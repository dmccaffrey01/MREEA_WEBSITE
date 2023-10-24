from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('date',)

admin.site.register(Event, EventAdmin)