from .models import Post, Category, Tag
from bs4 import BeautifulSoup
from datetime import datetime

def getArchives():
    dateFrom = datetime(2018, 1, 1)
    dateTo = datetime.today()

    archives = []
    months = [
        'January', 'February', 'March', 
        'April', 'May', 'June', 'July', 'August', 
        'September', 'October', 'November', 'December'
    ]
    for year in (dateFrom.year, dateTo.year):
        for i in range(12):
            archives.append({
                'year': year, 'month': i+1, 
                'yearmon': str(year) + " " + months[i]
            })
    return archives


def basicMiddleware(get_response):
    def middleware(request):
        posts = Post.objects.all()
        popular = Post.objects.order_by('-views')[:20]
        categories = Category.objects.all()
        latests = Post.objects.order_by('-pk')[:20]
        archives = getArchives()
        tags = Tag.objects.all()
        context = {'posts': posts, 
            'popular': popular,
            'categories': categories,
            'archives': archives,
            'tags': tags, 'latests': latests
        }
        request.context = context
        response = get_response(request)
        return response
    return middleware