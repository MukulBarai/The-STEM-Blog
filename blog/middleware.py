from .models import Post, Category, Tag
from bs4 import BeautifulSoup

def basicMiddleware(get_response):
    def middleware(request):
        posts = Post.objects.all()
        popular = Post.objects.order_by('-views')[:20]
        categories = Category.objects.all()
        latests = Post.objects.order_by('-pk')[:20]
        tags = Tag.objects.all()
        context = {'posts': posts, 
            'popular': popular,
            'categories': categories, 
            'tags': tags, 'latests': latests
        }
        request.context = context
        response = get_response(request)
        return response
    return middleware