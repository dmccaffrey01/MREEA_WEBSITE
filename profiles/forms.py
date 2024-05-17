from django import forms
from allauth.account.forms import SignupForm, ChangePasswordForm
from .models import UserProfile
from django.urls import reverse_lazy


class CustomPasswordChangeForm(ChangePasswordForm):
    def save(self):
        user = self.user
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.is_password_changed = True
        user_profile.save()
        super().save()
        return user
    

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name', required=True,
                                  widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, label='Last Name', required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    phone_number = forms.CharField(max_length=30, label='Phone Number', required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))

    def save(self, request):
        # Validate form data
        if not self.is_valid():
            raise ValueError("Form data is not valid")

        # Save the user
        user = super(CustomSignupForm, self).save(request)

        # Save additional user data
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        phone_number = self.cleaned_data['phone_number']
        
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.email = email
        profile.phone_number = phone_number
        profile.first_name = first_name
        profile.last_name = last_name
        profile.is_password_changed = True
        profile.save()

        return user
    

class EditProfileForm(forms.ModelForm):
    """ User profile form """

    class Meta:
        model = UserProfile
        exclude = ('user', 'image', 'classes', 'links', 'is_password_changed',)
