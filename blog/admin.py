from django.contrib import admin
from .models import Post, Category, Comment, CommentReply, ForbiddenWord, CategorySubscription

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_at', 'total_likes', 'total_dislikes']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content']

@admin.register(CommentReply)
class CommentReplyAdmin(admin.ModelAdmin):
    list_display = ['comment', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content']

@admin.register(ForbiddenWord)
class ForbiddenWordAdmin(admin.ModelAdmin):
    list_display = ['word', 'created_at']
    search_fields = ['word']

@admin.register(CategorySubscription)
class CategorySubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'subscribed_at']
    list_filter = ['category', 'subscribed_at']