from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from datetime import datetime, date

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

class PostForm(forms.Form):
    content = forms.CharField(
        max_length=1000,
        widget=forms.Textarea,
        label='Post Content'
    )
    title = forms.CharField(max_length=100, 
        label='Post Title')
    image = forms.CharField(max_length=1000,
        label='Image Url')
    category = forms.ChoiceField()
    published = forms.DateField(initial=date.today)
    tags = forms.CharField(max_length=100)
    views = forms.IntegerField(initial=0)
