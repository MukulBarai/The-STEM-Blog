from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .models import Post, Category, Tag, Comment
from .forms import SignUpForm, LoginForm
from django.core.paginator import Paginator
from django import forms
from django.db.models import Q

def index(request):
	context = request.context
	page = request.GET.get('page', 1)
	paginator = Paginator(context['posts'], 2)
	context['posts'] = paginator.page(page)
	return render(request, 'index.html', context)

def singlePost(request, id):
	context = request.context
	post = get_object_or_404(Post, pk=id)
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
	try:
		category = Category.objects.get(name=category)
	except Exception:
		posts = []
	else:
		posts = Post.objects.filter(category=category)
	page = request.GET.get('page', 1)
	paginator = Paginator(posts, 2)
	context['posts'] = paginator.page(page)
	context['category'] = category
	return render(request, 'category.html', context)

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
	context['word'] = word
	page = request.GET.get('page', 1)
	paginator = Paginator(posts, 2)
	context['posts'] = paginator.page(page)
	return render(request, 'search.html', context)

def addComment(request, id):
	context = request.context
	content = request.POST['content']
	author = request.user if request.user.is_authenticated else 'Guest'
	try:
		post = Post.objects.get(pk=id)
	except Exception:
		return redirect('singlepost', id=post.id)
	Comment.objects.create(content=content, author=author, post=post)
	return redirect('singlepost', id=post.id)

def tagPosts(request, tag):
	context = request.context
	try:
		tag = Tag.objects.get(name=tag)
	except Exception:
		posts = []
	else:
		posts = tag.posts.all()
	page = request.GET.get('page', 1)
	paginator = Paginator(posts, 2)
	context['posts'] = paginator.page(page)
	context['tag'] = tag
	return render(request, 'tag.html', context)

def error_404(request, message):
	context = request.context
	return render(request, '404.html', context)

def archive(request, year, month):
	context = request.context
	try:
		posts = Post.objects.filter(published__year=year, published__month=month)
	except Exception:
		posts = []
	page = request.GET.get('page', 1)
	paginator = Paginator(posts, 2)
	context['posts'] = paginator.page(page)
	return render(request, 'index.html', context)