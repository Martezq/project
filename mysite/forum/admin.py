from django.contrib import admin
from .models import Post, Comment, Topic

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('user', 'created_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    search_fields = ('content',)
    list_filter = ('user', 'post', 'created_at')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'created_at')
    list_filter = ('title', 'created_at')
