from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User
from .models import UserProfile, Category, Class


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name', required=True,
                                  widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, label='Last Name', required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['password2'].widget.attrs['placeholder'] = 'Password (confirmation)'

    def save(self, request):
        # Validate form data
        if not self.is_valid():
            raise ValueError("Form data is not valid")

        # Save the user
        user = super(CustomSignupForm, self).save(request)

        # Save additional user data
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.save()

        return user
    

class EditProfileForm(forms.ModelForm):
    """ User profile form """

    class Meta:
        model = UserProfile
        exclude = ('user', 'image', 'image_url', 'classes', 'links', )
