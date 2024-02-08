from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    """
    User Profile admin class
    """
    list_display = (
        'first_name',
        'last_name',
        'id',
        'username', 
    )

    # Define a function to retrieve the username from the user field
    def username(self, obj):
        return obj.user.username
    
    def first_name(self, obj):
        return obj.first_name
    
    def last_name(self, obj):
        return obj.last_name

    # Set the column name in the admin interface
    username.short_description = 'Username'
    first_name.short_description = 'First Name'
    last_name.short_description = 'Last Name'

admin.site.register(UserProfile, UserProfileAdmin)
