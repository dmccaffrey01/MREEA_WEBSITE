from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User


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