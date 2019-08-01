from django.shortcuts import render, redirect
from .models import Post, Category
# Create your views here.

def index(request):
	posts = Post.objects.all()
	categories = Category.objects.all()
	context = {
		'posts': posts, 
		'categories': categories,
	}
	return render(request, 'index.html', context)

def singlePost(request, id):
	post = Post.objects.get(pk=id)
	categories = Category.objects.all()
	context = {
		'post': post, 
		'categories': categories,
	}
	return render(request, 
		'posts/single.html', context)

def siteAdmin(request):
	if not request.user.is_authenticated:
		return redirect('/admin?next=/site/admin')
	posts = Post.objects.all()
	categories = Category.objects.all()
	context = {
		'posts': posts, 
		'categories': categories,
	}
	return render(request, 'admin/posts.html', context)

def posts(request):
	if not request.user.is_authenticated:
		return redirect('index')
	posts = Post.objects.all()
	categories = Category.objects.all()
	context = {
		'posts': posts, 
		'categories': categories,
	}
	return render(request, 
		'admin/posts.html', context)
def newPost(request):
	if not request.user.is_authenticated:
		return redirect('index')
	posts = Post.objects.all()
	categories = Category.objects.all()
	context = {
		'posts': posts, 
		'categories': categories,
	}
	return render(request, 'posts/newpost.html', context)

def categoryPosts(request, category):
	category = Category.objects.get(name=category)
	posts = Post.objects.filter(category=category.id)
	categories = Category.objects.all()
	context = {
		'posts': posts, 
		'categories': categories,
	}
	return render(request, 'index.html', context)
