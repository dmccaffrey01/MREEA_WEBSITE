from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('friendly_name','date', 'name')
    list_filter = ('date',)

admin.site.register(Event, EventAdmin)