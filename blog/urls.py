from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('category/<int:category_id>/', views.category_posts, name='category_posts'),
    path('search/', views.search, name='search'),
    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('dislike/<int:post_id>/', views.toggle_dislike, name='toggle_dislike'),
    path('subscribe/<int:category_id>/', views.toggle_subscription, name='toggle_subscription'),

    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-posts/', views.admin_posts, name='admin_posts'),
    path('admin-posts/create/', views.admin_post_create, name='admin_post_create'),
    path('admin-posts/<int:pk>/edit/', views.admin_post_edit, name='admin_post_edit'),
    path('admin-posts/<int:pk>/delete/', views.admin_post_delete, name='admin_post_delete'),
    path('admin-categories/', views.admin_categories, name='admin_categories'),
    path('admin-categories/create/', views.admin_category_create, name='admin_category_create'),
    path('admin-users/', views.admin_users, name='admin_users'),
    path('admin-users/<int:user_id>/toggle-block/', views.toggle_user_block, name='toggle_user_block'),
    path('admin-users/<int:user_id>/promote/', views.promote_user, name='promote_user'),
    path('admin-forbidden-words/', views.admin_forbidden_words, name='admin_forbidden_words'),
]