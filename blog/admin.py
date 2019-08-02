from django.contrib import admin
from .models import Post, Category, Tag, Comment
from django.contrib.sessions.models import Session

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Session)
admin.site.register(Tag)
admin.site.register(Comment)

