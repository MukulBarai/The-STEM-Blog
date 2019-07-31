from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date


class Menu(models.Model):
	title = models.CharField(max_length=100)
	def __str__(self): return self.title

class Category(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self): return self.name
	menu = models.ForeignKey(Menu,
		on_delete=models.CASCADE, null=True)

class Tag(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self): return self.name


class Post(models.Model):
	content = models.CharField(max_length=1000)
	title = models.CharField(max_length=100, 
		default='The title goes here')
	author = models.ForeignKey(User, 
		on_delete=models.CASCADE,related_name='post')
	image = models.CharField(max_length=1000)
	category = models.ForeignKey(Category,
		on_delete=models.CASCADE, related_name='category')
	published = models.DateField(default=date.today)
	tags = models.CharField(max_length=100, null=True)
	def __str__(self): return self.title