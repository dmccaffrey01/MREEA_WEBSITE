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

    category_name = forms.CharField(label="Category Name", max_length=100)
    class_name = forms.CharField(label="Class Name", max_length=100)

    class Meta:
        model = UserProfile
        exclude = ('user', 'image', 'image_url', 'category_field', 'class_field', 'full_name')

    def clean(self):
        cleaned_data = super().clean()
        category_name = cleaned_data.get("category_name")
        class_name = cleaned_data.get("class_name")

        if not Category.objects.filter(name=category_name).exists() and category_name != "none":
            raise forms.ValidationError("Invalid category selection. Please choose a valid category.")
        
        if not Class.objects.filter(name=class_name).exists() and class_name != "none":
            raise forms.ValidationError("Invalid class selection. Please choose a valid class.")
