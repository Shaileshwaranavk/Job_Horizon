from django import forms
from .models import UserProfile, OrganizationProfile
from django.contrib.auth.hashers import make_password

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    photo = forms.ImageField(required=True)
    resume = forms.FileField(required=True)

    class Meta:
        model = UserProfile
        fields = [
            'name', 'role', 'company_size', 'email', 'phone', 'password', 'gender',
            'experience', 'domains', 'expected_pay', 'projects', 'github',
            'portfolio', 'linkedin', 'photo', 'resume'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user_profile.password = make_password(self.cleaned_data['password'])
        if commit:
            user_profile.save()
        return user_profile

class OrganizationRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = OrganizationProfile
        fields = [
            'organization_name', 'manager_name', 'email', 'contact_number',
            'password', 'company_size', 'company_description', 'company_type'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if OrganizationProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered.")
        return email

    def save(self, commit=True):
        organization = super().save(commit=False)
        organization.password = make_password(self.cleaned_data['password'])
        if commit:
            organization.save()
        return organization
