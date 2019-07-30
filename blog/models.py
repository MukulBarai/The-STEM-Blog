from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date

class Post(models.Model):
	content = models.CharField(max_length=1000)
	title = models.CharField(max_length=100, null=True)
	author = models.ForeignKey(User, 
		on_delete=models.CASCADE,related_name='post')
	image = models.CharField(max_length=1000)
	published = models.DateField(default=date.today)

