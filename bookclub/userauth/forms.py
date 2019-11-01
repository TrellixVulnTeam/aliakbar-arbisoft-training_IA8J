from django.contrib.auth.models import User
from django import forms

from userauth.models import Profile


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ["username", "email", "password"]


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    fields = ['username', 'password']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["gender", "phone_number"]
