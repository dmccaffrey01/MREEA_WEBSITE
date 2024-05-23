from django import forms
from .models import Folder, Resource


class ManageResourceForm(forms.ModelForm):
    """ Event form """
    
    class Meta:
        model = Resource
        exclude = ('name', 'folder', 'icon', 'created_at',)
        widgets = {
            'friendly_name': forms.TextInput(attrs={'placeholder': 'Enter Name'}),
            'url': forms.TextInput(attrs={'placeholder': 'Enter URL'}),
        }


class ManageFolderForm(forms.ModelForm):
    """ Event form """
    
    class Meta:
        model = Folder
        exclude = ('name', 'parent_folder', 'icon', 'created_at',)
        widgets = {
            'friendly_name': forms.TextInput(attrs={'placeholder': 'Enter Name'}),
        }
