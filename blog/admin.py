from django.contrib import admin
from .models import Post, Category, Tag, Comment
from django.contrib.sessions.models import Session
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Session)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Permission)
admin.site.register(ContentType)
