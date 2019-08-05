from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .models import Post, Category, Tag, Comment
from .forms import SignUpForm, LoginForm, ProfileForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django import forms
from django.db.models import Q

def getPerPage():
    return 4

def index(request):
    context = request.context
    page = request.GET.get('page', 1)
    paginator = Paginator(context['posts'], getPerPage())
    context['posts'] = paginator.page(page)
    context['title'] = 'The times blog'
    return render(request, 'index.html', context)

def getRelatedPosts(post):
    tags = post.tags.all()
    posts = Post.objects.filter(tags__in=tags).exclude(pk=post.id).distinct()
    return posts

def singlePost(request, id):
    context = request.context
    post = get_object_or_404(Post, pk=id)
    post.views = post.views + 1
    post.save()
    context['post'] = post
    context['title'] = post.title
    context['relateds'] = getRelatedPosts(post)[0:5]
    return render(request, 'posts/single.html', context)

def categoryPosts(request, category):
    context = request.context
    context['title'] = 'Posts on ' + category
    try:
        newCategory = Category.objects.get(name=category)
    except Exception:
        posts = []
    else:
        posts = Post.objects.filter(category=newCategory)
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, getPerPage())
    context['posts'] = paginator.page(page)
    context['category'] = category
    return render(request, 'category.html', context)

def userSignup(request):
    context = request.context
    context['title'] = 'Sign Up'
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
        context['form'].non_field_errors = 'Cannot login new, please try again later'
        return render(request, 'registration/signup.html', context)
    login(request, user)
    return redirect('index')

def userLogin(request):
    context = request.context
    context['title'] = 'Log In'
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
    if user == None:
        form.non_field_errors = 'Username or Password is wrong'
        context['form'] = form
        return render(request, 'registration/login.html', context)
    login(request, user)
    return redirect('index')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/?next=/profile')
    context = request.context
    context['title'] = 'Your profile'
    if request.method == 'GET':
        return render(request, 'profile.html', context)
    form = ProfileForm(request.POST)
    if not form.is_valid():
        context['form'] = form
        return render(request, 'profile.html', context)
    username = form.cleaned_data.get('username')
    if User.objects.filter(username=username).exclude(pk=request.user.id):
        form.non_field_errors = 'User with this username already exists'
        context['form'] = form
        return render(request, 'profile.html', context)
    email = form.cleaned_data.get('email')
    first_name = form.cleaned_data.get('first_name')
    last_name = form.cleaned_data.get('last_name')
    user = User.objects.get(pk=request.user.id)
    user.username = username
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return redirect('profile')

def search(request):
    context = request.context
    word = request.GET['word']
    posts = Post.objects.filter(Q(content__icontains=word) | Q(title__icontains=word)).order_by('-views')[:20]
    context['word'] = word
    context['title'] = 'search for ' + word
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, getPerPage())
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
    context['title'] = 'Posts related to ' + tag
    try:
        newTag = Tag.objects.get(name=tag)
    except Exception:
        posts = []
    else:
        posts = newTag.posts.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, getPerPage())
    context['posts'] = paginator.page(page)
    context['tag'] = tag
    return render(request, 'tag.html', context)

def error_404(request, message):
    context = request.context
    return render(request, '404.html', context)

def getMonth(index):
    months = [
        'January', 'February', 'March', 
        'April', 'May', 'June', 'July', 
        'August', 'September', 'October', 
        'November', 'December'
    ]
    return months[index-1]

def archive(request, year, month):
    context = request.context
    context['title'] = 'Posts on' + getMonth(month) + ' ' + str(year)
    try:
        posts = Post.objects.filter(published__year=year, published__month=month)
    except Exception:
        posts = []
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, getPerPage())
    context['posts'] = paginator.page(page)
    return render(request, 'index.html', context)

def authorPosts(request, author):
    context = request.context
    context['title'] = 'Posts by ' + author
    newAuthor = get_object_or_404(User, username=author)
    posts = Post.objects.filter(author=newAuthor)
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, getPerPage())
    context['posts'] = paginator.page(page)
    context['author'] = author
    return render(request, 'author.html', context)