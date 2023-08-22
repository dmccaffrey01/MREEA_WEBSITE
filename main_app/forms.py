from django import forms
from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth.models import User
from .models import Event, MemberProfile, ContactMessage


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    phone_number = forms.CharField(max_length=15, label='Phone Number')

    def custom_signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.save()

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        self.custom_signup(request, user)
        return user
    

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'start_date', 'end_date', 'location', 'event_image_change')


class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ('first_name', 'last_name', 'bio', 'display_email', 'email', 'display_number', 'phone_number', 'website', 'facebook')


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']


class MemberSearchForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ('last_name', 'first_name', 'teaching_category', 'classes')


class MemberProfilePictureForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ['profile_image_change']