from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
]