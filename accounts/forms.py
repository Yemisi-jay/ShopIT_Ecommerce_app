from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number', 'address', 'city', 'state', 'country', 'zip_code')
