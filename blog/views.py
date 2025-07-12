from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Post, Category, Comment, CommentReply, CategorySubscription, ForbiddenWord
from .forms import PostForm, CategoryForm, CommentForm, CommentReplyForm

User = get_user_model()


def home(request):
    posts = Post.objects.select_related('author', 'category').all()
    categories = Category.objects.all()

    # Get user subscriptions
    user_subscriptions = []
    if request.user.is_authenticated:
        user_subscriptions = CategorySubscription.objects.filter(
            user=request.user
        ).values_list('category_id', flat=True)

    # Pagination
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'user_subscriptions': user_subscriptions,
    }
    return render(request, 'blog/home.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).select_related('author')

    comment_form = CommentForm()
    reply_form = CommentReplyForm()

    if request.method == 'POST':
        if 'comment_form' in request.POST and request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('blog:post_detail', pk=pk)
        elif 'reply_form' in request.POST and request.user.is_authenticated:
            reply_form = CommentReplyForm(request.POST)
            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.comment_id = request.POST.get('comment_id')
                reply.author = request.user
                reply.save()
                return redirect('blog:post_detail', pk=pk)

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'reply_form': reply_form,
    }
    return render(request, 'blog/post_detail.html', context)


def category_posts(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    posts = Post.objects.filter(category=category).select_related('author')

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category_posts.html', context)


def search(request):
    query = request.GET.get('q', '')
    posts = Post.objects.none()

    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(tags__icontains=query)
        ).select_related('author', 'category')

    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'blog/search.html', context)


@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        post.dislikes.remove(request.user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'likes_count': post.total_likes(),
        'dislikes_count': post.total_dislikes(),
    })


@login_required
@require_POST
def toggle_dislike(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
        disliked = False
    else:
        post.dislikes.add(request.user)
        post.likes.remove(request.user)
        disliked = True

    # Check if post should be auto-deleted
    if post.total_dislikes() > 10:
        post.delete()
        return JsonResponse({'deleted': True})

    return JsonResponse({
        'disliked': disliked,
        'likes_count': post.total_likes(),
        'dislikes_count': post.total_dislikes(),
    })


@login_required
@require_POST
def toggle_subscription(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    subscription, created = CategorySubscription.objects.get_or_create(
        user=request.user,
        category=category
    )

    if not created:
        subscription.delete()
        subscribed = False
    else:
        subscribed = True
        # Send confirmation email
        send_mail(
            subject='Subscription Confirmation',
            message=f'Hello {request.user.username}, you have subscribed successfully to {category.name}. Welcome aboard!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
        )

    return JsonResponse({'subscribed': subscribed})


# Admin Views
def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin)
def admin_dashboard(request):
    posts_count = Post.objects.count()
    categories_count = Category.objects.count()
    users_count = User.objects.count()
    comments_count = Comment.objects.count()

    context = {
        'posts_count': posts_count,
        'categories_count': categories_count,
        'users_count': users_count,
        'comments_count': comments_count,
    }
    return render(request, 'blog/admin/dashboard.html', context)


@user_passes_test(is_admin)
def admin_posts(request):
    posts = Post.objects.select_related('author', 'category').all()
    return render(request, 'blog/admin/posts.html', {'posts': posts})


@user_passes_test(is_admin)
def admin_post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('blog:admin_posts')
    else:
        form = PostForm()
    return render(request, 'blog/admin/post_form.html', {'form': form, 'title': 'Create Post'})


@user_passes_test(is_admin)
def admin_post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('blog:admin_posts')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/admin/post_form.html', {'form': form, 'title': 'Edit Post'})


@user_passes_test(is_admin)
def admin_post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('blog:admin_posts')
    return render(request, 'blog/admin/post_confirm_delete.html', {'post': post})


@user_passes_test(is_admin)
def admin_categories(request):
    categories = Category.objects.all()
    return render(request, 'blog/admin/categories.html', {'categories': categories})


@user_passes_test(is_admin)
def admin_category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('blog:admin_categories')
    else:
        form = CategoryForm()
    return render(request, 'blog/admin/category_form.html', {'form': form, 'title': 'Create Category'})


@user_passes_test(is_admin)
def admin_users(request):
    users = User.objects.all()
    return render(request, 'blog/admin/users.html', {'users': users})


@user_passes_test(is_admin)
def toggle_user_block(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if not user.is_staff:  # Can't block admin users
        user.is_blocked = not user.is_blocked
        user.save()
        status = 'blocked' if user.is_blocked else 'unblocked'
        messages.success(request, f'User {user.username} has been {status}.')
    return redirect('blog:admin_users')


@user_passes_test(is_admin)
def promote_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_staff = True
    user.save()
    messages.success(request, f'User {user.username} has been promoted to admin.')
    return redirect('blog:admin_users')


@user_passes_test(is_admin)
def admin_forbidden_words(request):
    words = ForbiddenWord.objects.all()
    return render(request, 'blog/admin/forbidden_words.html', {'words': words})

@user_passes_test(is_admin)
def admin_forbidden_words(request):
    if request.method == 'POST':
        word = request.POST.get('word', '').strip().lower()
        if word:
            forbidden_word, created = ForbiddenWord.objects.get_or_create(word=word)
            if created:
                messages.success(request, f'Word "{word}" added to forbidden list.')
            else:
                messages.warning(request, f'Word "{word}" already exists.')
        return redirect('blog:admin_forbidden_words')
    
    words = ForbiddenWord.objects.all()
    return render(request, 'blog/admin/forbidden_words.html', {'words': words})