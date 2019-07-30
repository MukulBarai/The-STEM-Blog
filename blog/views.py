from django.shortcuts import render
from .models import Post, Category, Menu
# Create your views here.

def index(request):
	posts = Post.objects.all()
	categories = Category.objects.all()
	menus = Menu.objects.all()
	context = {
		'posts': posts, 
		'categories': categories,
		'menus': menus
	}
	return render(request, 
		'index.html', context)