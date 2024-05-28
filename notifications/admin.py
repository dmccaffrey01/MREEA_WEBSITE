from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'date', 
    )

    # Define a function to retrieve the username from the user field
    def first_name(self, obj):
        return obj.user.first_name
    
    def last_name(self, obj):
        return obj.user.last_name
    
    # Set the column name in the admin interface
    first_name.short_description = 'First Name'
    last_name.short_description = 'Last Name'


admin.site.register(Notification, NotificationAdmin)
