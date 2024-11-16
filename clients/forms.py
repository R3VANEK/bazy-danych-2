from django import forms
from django.contrib.auth import authenticate


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
