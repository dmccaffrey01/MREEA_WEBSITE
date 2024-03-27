from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'status',
        'date', 
    )

    # Define a function to retrieve the username from the user field
    def first_name(self, obj):
        return obj.user.first_name
    
    def last_name(self, obj):
        return obj.user.last_name
    
    def status(self, obj):
        return obj.read_status


    # Set the column name in the admin interface
    first_name.short_description = 'First Name'
    last_name.short_description = 'Last Name'
    status.short_description = 'Last Name'



admin.site.register(Notification, NotificationAdmin)
