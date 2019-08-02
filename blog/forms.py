from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from datetime import datetime, date
from .models import Post, Category

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, 
    	required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, 
    	required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, 
    	help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = (
        	'username', 'first_name', 'last_name', 
        	'email', 'password1', 'password2', 
        )


class PostForm(ModelForm):
    content = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={'row': '2'})
    )
    class Meta:
        model = Post
        fields = (
            'content', 'title', 
            'image', 'category', 'tags'
        )
 