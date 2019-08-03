from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import Post, Category, Tag, Comment
from .forms import SignUpForm, LoginForm
from django import forms
from django.db.models import Q

def index(request):
	context = request.context
	return render(request, 'index.html', context)

def singlePost(request, id):
	context = request.context
	post = Post.objects.get(pk=id)
	post.views = post.views + 1
	post.save()
	context['post'] = post
	return render(request, 
		'posts/single.html', context)

def siteAdmin(request):
	context = request.context
	if not request.user.is_authenticated:
		return redirect('/admin/login/?next=/site/admin')
	return render(request, 'admin/posts.html', context)

def posts(request):
	context = request.context
	if not request.user.is_authenticated:
		return redirect('index')
	return render(request, 
		'admin/posts.html', context)

def categoryPosts(request, category):
	context = request.context
	category = Category.objects.get(name=category)
	posts = Post.objects.filter(category=category.id)
	context['posts'] = posts
	return render(request, 'index.html', context)

def userSignup(request):
	context = request.context
	if request.user.is_authenticated: 
		return redirect('index')
	if request.method == 'GET':
		form = SignUpForm()
		context['form'] = form
		return render(request, 'registration/signup.html', context)
	form = SignUpForm(request.POST)
	if not form.is_valid():
		context['form'] = form
		return render(request, 'registration/signup.html', context)
	form.save()
	username = form.cleaned_data.get('username')
	password = form.cleaned_data.get('password1')
	user = authenticate(username=username, password=password)
	if user == None:
		context.form.non_field_errors = 'Cannot login new, please try again later'
		return render(request, 'registration/signup.html', context)
	login(request, user)
	return redirect('index')

def userLogin(request):
	context = request.context
	if request.user.is_authenticated:
		return redirect('index')
	if request.method == 'GET':
		form = LoginForm()
		context['form'] = form
		return render(request, 'registration/login.html', context)
	form = LoginForm(request.POST)
	if not form.is_valid():
		context['form'] = form
		return render(request, 'registration/login.html', context)
	username = form.cleaned_data.get('username')
	password = form.cleaned_data.get('password')
	user = authenticate(username=username, password=password)
	print(user)
	if user == None:
		context['errors'] = 'Username or Password is wrong'
		return render(request, 'registration/login.html', context)
	login(request, user)
	return redirect('index')

def profile(request):
	if not request.user.is_authenticated:
		return redirect('/accounts/login/?next=/profile')
	context = request.context
	return render(request, 'profile.html', context)

def search(request):
	context = request.context
	word = request.GET['word']
	posts = Post.objects.filter(Q(content__icontains=word) | Q(title__icontains=word)).order_by('-views')[:20]
	context['posts'] = posts
	return render(request, 'search.html', context)

def addComment(request, id):
	context = request.context
	content = request.POST['content']
	author = request.user if request.user.is_authenticated else 'Guest'
	post = Post.objects.get(pk=id)
	Comment.objects.create(content=content, author=author, post=post)
	return redirect('singlepost', id=post.id)

def tagPosts(request, tag):
	context = request.context
	tag = Tag.objects.get(name=tag)
	posts = tag.posts.all()
	context['posts'] = posts
	return render(request, 'index.html', context)