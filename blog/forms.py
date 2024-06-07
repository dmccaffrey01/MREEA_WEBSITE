from django import forms
from .models import BlogPost
from .widgets import CustomCKEditor5Widget

class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=CustomCKEditor5Widget())

    class Meta:
        model = BlogPost
        fields = ['title', 'content']