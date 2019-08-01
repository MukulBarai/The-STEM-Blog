from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import Post, Category
from .forms import SignUpForm, PostForm
from django import forms
import json

def index(request):
	posts = Post.objects.all()
	popular = Post.objects.order_by('-views')[:20]
	categories = Category.objects.all()
	context = {
		'posts': posts, 
		'categories': categories,
		'popular': popular
	}
	return render(request, 'index.html', context)

def singlePost(request, id):
	post = Post.objects.get(pk=id)
	popular = Post.objects.order_by('-views')[:20]
	categories = Category.objects.all()
	context = {
		'post': post, 
		'categories': categories,
		'popular': popular
	}
	return render(request, 
		'posts/single.html', context)

def siteAdmin(request):
	if not request.user.is_authenticated:
		return redirect('/admin?next=/site/admin')
	posts = Post.objects.all()
	categories = Category.objects.all()
	popular = Post.objects.order_by('-views')[:20]
	context = {
		'posts': posts, 
		'categories': categories,
		'popular': popular
	}
	return render(request, 'admin/posts.html', context)

def posts(request):
	if not request.user.is_authenticated:
		return redirect('index')
	posts = Post.objects.all()
	categories = Category.objects.all()
	popular = Post.objects.order_by('-views')[:20]
	context = {
		'posts': posts, 
		'categories': categories,
		'popular': popular
	}
	return render(request, 
		'admin/posts.html', context)
def newPost(request):
	if not request.user.is_authenticated:
		return redirect('index')
	posts = Post.objects.all()
	categories = Category.objects.all()
	popular = Post.objects.order_by('-views')[:20]
	if request.method == 'GET':
		form = PostForm()
		context = {
			'posts': posts, 
			'categories': categories,
			'popular': popular,
			'form': form
		}
		return render(request, 'posts/newpost.html', context)
	form = PostForm(request.POST)
	if not form.is_valid():
		context = {
		'posts': posts, 
		'categories': categories,
		'popular': popular,
		'form': form
		}
		return render(request, 'posts/newpost.html', context)
	post = form.save(commit=False)
	post.author = request.user
	post.save()
	posts = Post.objects.all()
	context = {
		'posts': posts, 
		'categories': categories,
		'popular': popular,
		'form': form
	}
	return redirect('posts') 

def categoryPosts(request, category):
	category = Category.objects.get(name=category)
	posts = Post.objects.filter(category=category.id)
	popular = Post.objects.order_by('-views')[:20]
	categories = Category.objects.all()
	context = {
		'posts': posts, 
		'categories': categories,
		'popular': popular
	}
	return render(request, 'index.html', context)

def signup(request):
	categories = Category.objects.all()
	if request.user.is_authenticated: 
		return redirect('index')
	if request.method == 'GET':
		form = SignUpForm()
		context = {'form': form, 'categories': categories}
		print(categories)
		return render(request, 'registration/signup.html', context)
	form = SignUpForm(request.POST)
	if not form.is_valid():
		context = {'form': form, 'categories': categories}
		return render(request, 'registration/signup.html', context)
	form.save()
	username = form.cleaned_data.get('username')
	password = form.cleaned_data.get('password1')
	user = authenticate(username=username, password=password)
	login(request, user)
	return redirect('index')
