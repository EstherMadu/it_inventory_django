from django import forms
from django.contrib.auth.models import User
from .models import Asset, AssetCategory, AssetStatus,Vendor

class AdminSignupForm(forms.Form):
    username = forms.CharField(max_length=75)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    department = forms.CharField(max_length=100)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match")
        return cleaned

class AdminLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class VendorSignupForm(forms.ModelForm):
    username = forms.CharField(max_length=75)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    vendor_confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match")
        return cleaned

    # class Meta:
    #     model = Vendor
    #     fields = ['vendor_name', 'vendor_email', 'vendor_password']

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name','serial_number','model_number','make','picture','category','vendor','quantity','current_status','current_holder']
        widgets = {
            'current_status': forms.Select(choices=AssetStatus.choices),
        }

class AssignmentForm(forms.Form):
    assigned_to = forms.CharField(max_length=128)
    assigned_by = forms.CharField(max_length=128, required=False)
    note = forms.CharField(max_length=256, required=False)

class VendorForm(forms.Form):
    username = forms.CharField(max_length=75)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=6)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match")
        return cleaned
    
class VendorLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)