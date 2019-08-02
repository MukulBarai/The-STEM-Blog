from .models import Post, Category, Tag

def basicMiddleware(get_response):
    def middleware(request):
        posts = Post.objects.all()
        popular = Post.objects.order_by('-views')[:20]
        categories = Category.objects.all()
        tags = Tag.objects.all()
        context = {'posts': posts, 'popular': popular,
            'categories': categories, 'tags': tags
        }
        request.context = context
        response = get_response(request)
        return response
    return middleware