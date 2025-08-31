from django.urls import path
from .views import PostListCreateView, PostDetailView, FeedView
from .views_html import post_list_view, create_post_view, my_posts_view, edit_post_view, delete_post_view

urlpatterns = [
    path('', post_list_view, name='post_list'),
    path('create/', create_post_view, name='create_post'),
    path('my-posts/', my_posts_view, name='my_posts'),
    path('edit/<int:post_id>/', edit_post_view, name='edit_post'),
    path('api/', PostListCreateView.as_view(), name='api-post-list-create'),
    path('api/<int:pk>/', PostDetailView.as_view(), name='api-post-detail'),
    path('api/feed/', FeedView.as_view(), name='api-feed'),
    path('delete/<int:post_id>/', delete_post_view, name='delete_post'),
]
