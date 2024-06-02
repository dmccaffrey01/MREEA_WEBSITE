from django.contrib import admin
from .models import Membership, MembershipPackage, MembershipStatus
from django import forms


class MembershipPackageAdminForm(forms.ModelForm):
    class Meta:
        model = MembershipPackage
        fields = '__all__'
        labels = {
            'duration': 'Duration (days)',
            'price': 'Price ($USD)',
        }


class MembershipPackageAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'name', 'get_duration', 'get_price',)
    ordering = ('price', 'friendly_name', 'name',)

    def get_duration(self, obj):
        return obj.duration
    get_duration.short_description = 'Duration (days)'

    def get_price(self, obj):
        return obj.price
    get_price.short_description = 'Price ($USD)'

class MembershipStatusAdmin(admin.ModelAdmin):
    verbose_name_plural = 'Membership statuses'
    list_display = ('friendly_name', 'name', 'valid',)
    ordering = ('friendly_name', 'name',)


class MembershipAdmin(admin.ModelAdmin):
    fields = ('user', 'package', 'status', 'purchase_date', 'start_date', 'end_date',)
    list_display = ('get_user_first_name', 'get_user_last_name', 'get_user_email', 'purchase_date', 'end_date',)
    search_fields = ['user__first_name', 'user__last_name', 'user__email',]

    def get_user_first_name(self, obj):
        return obj.user.first_name
    get_user_first_name.short_description = 'First Name'

    def get_user_last_name(self, obj):
        return obj.user.last_name
    get_user_last_name.short_description = 'Last Name'

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'Email'

admin.site.register(Membership, MembershipAdmin)
admin.site.register(MembershipPackage, MembershipPackageAdmin)
admin.site.register(MembershipStatus, MembershipStatusAdmin)
