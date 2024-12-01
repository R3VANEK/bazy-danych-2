from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Driver

class DriverLoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        client = authenticate(username=username, password=password)
        if client is None:
            raise forms.ValidationError("Invalid login credentials.")
        return self.cleaned_data

class DriverRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, help_text="")
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    license_expiration = forms.DateTimeField(required=True)
    is_male = forms.BooleanField(required=True)

    class Meta:
        model = Driver
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'license_expiration', 'is_male']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        driver = super().save(commit=False)
        driver.user = user
        if commit:
            driver.save()
        return driver