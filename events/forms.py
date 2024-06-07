from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    """ Event form """
    
    date = forms.DateField(
        input_formats=['%m/%d/%Y'],  # Specify the input format
        widget=forms.DateInput(attrs={'placeholder': 'Enter Date: MM/DD/YYYY'})
    )

    time = forms.TimeField(
        input_formats=['%H:%M'],  # Specify the input format for HH:MM
        widget=forms.TimeInput(attrs={'placeholder': 'Enter Time: HH:MM'})
    )

    class Meta:
        model = Event
        exclude = ('name', 'register_link', 'google_drive_link', 'folder',)
        widgets = {
            'friendly_name': forms.TextInput(attrs={'placeholder': 'Enter Name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter Description', 'rows': 8}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter Location'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.date:
            self.initial['date'] = self.instance.date.strftime('%m/%d/%Y')
        if self.instance and self.instance.time:
            self.initial['time'] = self.instance.time.strftime('%H:%M')

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date:
            return date.strftime('%Y-%m-%d')
        return date
