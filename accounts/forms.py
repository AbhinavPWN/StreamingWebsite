from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(required=True)
    subscription_type = forms.ChoiceField(choices=[('streamer', 'Streamer'), ('viewer', 'Viewer')])

    class Meta:
        model = User
        fields = ('username', 'email', 'date_of_birth', 'password1', 'password2', 'subscription_type')


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
