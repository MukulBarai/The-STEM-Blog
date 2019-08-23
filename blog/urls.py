from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('search/', views.search, name='search'),
	path('accounts/login/', views.userLogin, name='login'),
	path('accounts/', include('django.contrib.auth.urls')),
	path('accounts/profile/', views.profile, name='profile'),
	path('accounts/signup/', views.userSignup, name='signup'),
	path('posts/archive/<int:year>/<int:month>/', views.archive, name='archive'),
	path('posts/<int:id>/<slug:slug>/', views.singlePost, name='singlepost'),
	path('categories/<str:category>/', views.categoryPosts, name='category'),
	path('tags/<str:tag>/', views.tagPosts, name='tags'),
	path('posts/addcomment/<int:id>/', views.addComment, name='addcomment'),
	path('posts/author/<str:author>/', views.authorPosts, name='author'),
]