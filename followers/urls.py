# followers/urls.py

from django.urls import path
from .views import FollowingListCreateView, UnfollowView

urlpatterns = [
    # List who the authenticated user is following and create new follow relationships
    path('', FollowingListCreateView.as_view(), name='following-list-create'),

    # Unfollow a specific user by their ID
    path('unfollow/<int:following_id>/', UnfollowView.as_view(), name='unfollow-user'),
]