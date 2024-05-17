from django.contrib import admin
from .models import UserProfile, Category, Class, ProfileLink, TeachingState


class UserProfileAdmin(admin.ModelAdmin):
    """
    User Profile admin class
    """
    list_display = (
        'first_name',
        'last_name',
        'get_email',
        'id',
        'username', 
    )

    # Define a function to retrieve the username from the user field
    def username(self, obj):
        return obj.user.username
    
    def get_email(self, obj):
        return obj.user.email
    
    def first_name(self, obj):
        return obj.first_name
    
    def last_name(self, obj):
        return obj.last_name

    # Set the column name in the admin interface
    username.short_description = 'Username'
    first_name.short_description = 'First Name'
    last_name.short_description = 'Last Name'
    get_email.short_description = 'Email'


class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name_plural = 'Categories'

    list_display = ('friendly_name', 'name',)


class TeachingStateAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name_plural = 'Teaching States'

    list_display = ('friendly_name', 'code',)


class ClassAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name_plural = 'Classes'

    list_display = ('friendly_name', 'name',)


class ProfileLinkAdmin(admin.ModelAdmin):

    list_display = ('first_name', 'last_name', 'friendly_name', 'url',)
    
    def first_name(self, obj):
        return obj.user.first_name
    
    def last_name(self, obj):
        return obj.user.last_name

    # Set the column name in the admin interface
    first_name.short_description = 'First Name'
    last_name.short_description = 'Last Name'


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(TeachingState, TeachingStateAdmin)
admin.site.register(ProfileLink, ProfileLinkAdmin)
