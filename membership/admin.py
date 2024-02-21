from django.contrib import admin
from .models import Membership, MembershipPackage, MembershipStatus, MembershipUpdateStatus
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


class MembershipUpdateStatusAdmin(admin.ModelAdmin):
    verbose_name_plural = 'Membership Updates'
    list_display = ('friendly_name', 'name', 'last_updated_date',)
    readonly_fields = ('name', 'friendly_name', 'last_updated_date')
                       

class MembershipAdmin(admin.ModelAdmin):
    readonly_fields = ('is_valid', 'cost', 'start_date',)
    fields = ('user', 'package', 'cost', 'status', 'is_valid', 'purchase_date', 'start_date', 'end_date',)
    list_display = ('get_user_first_name', 'get_user_last_name', 'get_user_email', 'get_user_username', 'purchase_date', 'end_date', 'is_valid', 'get_status_friendly_name',)
    ordering = ('-is_valid','-purchase_date', '-end_date')
    list_filter = ('status__friendly_name', 'is_valid')
    search_fields = ['user__first_name', 'user__last_name', 'user__username']
    actions = ['set_status_active', 'set_status_payment_unsuccessful', 'set_status_active_renewal_unsuccessful']

    def get_user_first_name(self, obj):
        return obj.user.first_name
    get_user_first_name.short_description = 'First Name'

    def get_user_last_name(self, obj):
        return obj.user.last_name
    get_user_last_name.short_description = 'Last Name'

    def get_user_username(self, obj):
        return obj.user.username
    get_user_username.short_description = 'Username'

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'Email'

    def get_status_friendly_name(self, obj):
        return obj.status.friendly_name
    get_status_friendly_name.short_description = 'Status'

    def set_status_active(self, request, queryset):
        active_status = MembershipStatus.objects.get(name='active')
        queryset.update(status=active_status)
    set_status_active.short_description = "Set Status to Active"

    def set_status_payment_unsuccessful(self, request, queryset):
        payment_unsuccessful_status = MembershipStatus.objects.get(name='payment_unsuccessful')
        queryset.update(status=payment_unsuccessful_status)
    set_status_payment_unsuccessful.short_description = "Set Status to Payment Unsuccessful"

    def set_status_active_renewal_unsuccessful(self, request, queryset):
        active_renewal_unsuccessful_status = MembershipStatus.objects.get(name='active_renewal_unsuccessful')
        queryset.update(status=active_renewal_unsuccessful_status)
    set_status_active_renewal_unsuccessful.short_description = "Set Status to Active Renewal Unsuccessful"


    autocomplete_fields = ['user']

    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name} - ({obj.user.username})"
    user_full_name.short_description = 'User'

admin.site.register(Membership, MembershipAdmin)
admin.site.register(MembershipPackage, MembershipPackageAdmin)
admin.site.register(MembershipStatus, MembershipStatusAdmin)
admin.site.register(MembershipUpdateStatus, MembershipUpdateStatusAdmin)
