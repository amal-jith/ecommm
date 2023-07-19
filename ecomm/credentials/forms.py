from django import forms
from credentials.models import CustomUser
class RegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        # Check if the username is already taken
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Username is already taken.')
        return username


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
