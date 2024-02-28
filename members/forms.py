from django import forms
from profiles.models import UserProfile, Category, Class

class MembersSearchForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=254, required=False)
    last_name = forms.CharField(label="Last Name", max_length=254, required=False)
    category_name = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Category Name",
        to_field_name="name",
        empty_label="Select",
        required=False,
        widget=forms.Select(attrs={'class': 'custom-select'}),
    )
    class_name = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        label="Class Name",
        to_field_name="name",
        empty_label="Select",
        required=False,
        widget=forms.Select(attrs={'class': 'custom-select'}),
    )

    def __init__(self, *args, **kwargs):
        super(MembersSearchForm, self).__init__(*args, **kwargs)
        self.fields['category_name'].label_from_instance = lambda obj: obj.friendly_name
        self.fields['class_name'].label_from_instance = lambda obj: obj.friendly_name
