from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('accounts/', include('django.contrib.auth.urls')),
	path('posts/<int:id>/', views.singlePost, name='singlepost'),
	path('site/admin/', views.siteAdmin, name='siteadmin'),
	path('site/admin/posts/', views.posts, name='posts'),
	path('site/admin/posts/new', views.newPost, name='newpost'),
	path('posts/<str:category>/', views.categoryPosts, name='category'),
]