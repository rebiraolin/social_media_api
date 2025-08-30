from django.urls import path
from .views import PostListCreateView, PostDetailView, FeedView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post_list_create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('feed/', FeedView.as_view(), name='feed'),
]