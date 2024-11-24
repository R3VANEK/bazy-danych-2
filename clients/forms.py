from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Client

# Formularz logowania klienta
class ClientLoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        # Autoryzacja klienta
        client = authenticate(username=username, password=password)
        if client is None:
            raise forms.ValidationError("Invalid login credentials.")
        return self.cleaned_data

# Formularz rejestracji klienta
class ClientRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, help_text="")
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = Client
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'phone_number']

    def save(self, commit=True):
        # Tworzenie użytkownika Django
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        # Tworzenie rekordu klienta
        client = super().save(commit=False)
        client.user = user
        if commit:
            client.save()
        return client
