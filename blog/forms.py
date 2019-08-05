from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from datetime import datetime, date
from .models import Post, Category

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)

class ProfileForm(ModelForm):
    username = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    date_joined = forms.DateTimeField()
    last_login = forms.DateTimeField()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username already exists")
        return username