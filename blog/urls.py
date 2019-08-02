from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('accounts/', include('django.contrib.auth.urls')),
	path('accounts/profile/', views.profile, name='profile'),
	path('accounts/signup/', views.signup, name='signup'),
	path('posts/<int:id>/', views.singlePost, name='singlepost'),
	path('posts/<str:category>/', views.categoryPosts, name='category'),
]