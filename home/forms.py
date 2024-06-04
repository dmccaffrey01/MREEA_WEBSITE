from django import forms
from .models import Testimonial


class TestimonialForm(forms.ModelForm):
    """
    Class for the Testimonial form model
    """
    class Meta:
        model = Testimonial
        exclude = ('user',)
        widgets = {
            'message': forms.Textarea(attrs={'placeholder': 'Enter Message', 'rows': 8}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['message'].widget.attrs['autofocus'] = True