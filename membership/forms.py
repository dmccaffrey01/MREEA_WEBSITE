from django import forms
from .models import MembershipPackage


class MembershipPackageForm(forms.Form):
    package_name = forms.CharField(label="Package Name", max_length=100)

    def clean(self):
        cleaned_data = super().clean()
        package_name = cleaned_data.get("package_name")

        if not MembershipPackage.objects.filter(name=package_name,).exists():
            raise forms.ValidationError("Invalid package selection. Please choose a valid package.")