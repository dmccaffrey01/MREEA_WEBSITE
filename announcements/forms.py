from django import forms
from .models import Announcement


class AnnouncementForm(forms.ModelForm):
    """ Announcement form """
    
    class Meta:
        model = Announcement
        exclude = ('name', 'date_made_public', 'folder',)
        widgets = {
            'friendly_name': forms.TextInput(attrs={'placeholder': 'Enter Name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter Description', 'rows': 8}),
        }