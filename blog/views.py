from django.shortcuts import render
from .models import Post, Category
# Create your views here.

def index(request):
	posts = Post.objects.all()
	categories = Category.objects.all()
	context = {'posts': posts, 
		'categories': categories}
	return render(request, 
		'index.html', context)