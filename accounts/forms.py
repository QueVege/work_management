from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class AuthForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    fields = ['username', 'password']
    
    def get_user(self):
        user = authenticate(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'])
        return user
