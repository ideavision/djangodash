from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from authentication.models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control"
            }
        ))
    phone_number = PhoneNumberField(
        widget=PhoneNumberInternationalFallbackWidget(
            attrs={
                "placeholder" : "Phone Number",                
                "class": "form-control"
            }
        ))
    website_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Website Name",                
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password check",                
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=True)
        profile = UserProfile.objects.create(user=user)
        phone_number = self.cleaned_data['phone_number']
        website_name = self.cleaned_data['website_name']
        if phone_number and website_name:
            profile.phone_number = self.cleaned_data['phone_number']
            profile.website_name = self.cleaned_data['website_name']
            profile.save()
        return user