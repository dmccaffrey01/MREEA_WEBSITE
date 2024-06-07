from django import forms

class CustomCKEditor5Widget(forms.Textarea):
    template_name = 'widgets/custom_ckeditor5_widget.html'

    class Media:
        js = (
            'ckeditor5/ckeditor.js',  # Path to your CKEditor 5 build
        )