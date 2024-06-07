from django import forms
from .models import MembershipPackage, Membership


class MembershipPackageForm(forms.Form):
    package_name = forms.CharField(label="Package Name", max_length=100)

    def clean(self):
        cleaned_data = super().clean()
        package_name = cleaned_data.get("package_name")

        if not MembershipPackage.objects.filter(name=package_name,).exists():
            raise forms.ValidationError("Invalid package selection. Please choose a valid package.")
        

class MembershipForm(forms.ModelForm):
    
    purchase_date = forms.DateField(
        input_formats=['%m/%d/%Y'],  # Specify the input format
        widget=forms.DateInput(attrs={'placeholder': 'Enter Date: MM/DD/YYYY'})
    )

    start_date = forms.DateField(
        input_formats=['%m/%d/%Y'],  # Specify the input format
        widget=forms.DateInput(attrs={'placeholder': 'Enter Date: MM/DD/YYYY'})
    )

    end_date = forms.DateField(
        input_formats=['%m/%d/%Y'],  # Specify the input format
        widget=forms.DateInput(attrs={'placeholder': 'Enter Date: MM/DD/YYYY'})
    )

    class Meta:
        model = Membership
        exclude = ('user', 'package', 'status', 'status_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.purchase_date:
            self.initial['purchase_date'] = self.instance.purchase_date.strftime('%m/%d/%Y')
        if self.instance and self.instance.start_date:
            self.initial['start_date'] = self.instance.start_date.strftime('%m/%d/%Y')
        if self.instance and self.instance.end_date:
            self.initial['end_date'] = self.instance.end_date.strftime('%m/%d/%Y')

    def clean_purchase_date(self):
        purchase_date = self.cleaned_data.get('purchase_date')
        if purchase_date:
            return purchase_date.strftime('%Y-%m-%d')
        return purchase_date
    
    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date:
            return start_date.strftime('%Y-%m-%d')
        return start_date
    
    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        if end_date:
            return end_date.strftime('%Y-%m-%d')
        return end_date