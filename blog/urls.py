from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('settings/', views.settings, name='settings'),
	path('accounts/', include('django.contrib.auth.urls')),
	path('accounts/signup/', views.signup, name='signup'),
	path('posts/<int:id>/', views.singlePost, name='singlepost'),
	path('posts/<str:category>/', views.categoryPosts, name='category'),
]