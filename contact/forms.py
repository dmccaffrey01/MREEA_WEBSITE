from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """
    Class for the Contact form model
    """
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Enter Email'}),
            'message': forms.Textarea(attrs={'placeholder': 'Enter Message', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['autofocus'] = True