from django.urls import path
from .views import FollowingListCreateView, UnfollowView
from .views_html import following_list_view, unfollow_user_view

urlpatterns = [
    path('api/', FollowingListCreateView.as_view(), name='following-list-create-api'),
    path('api/unfollow/<int:following_id>/', UnfollowView.as_view(), name='unfollow-user-api'),
    path('', following_list_view, name='following-list'),
    path('unfollow/<int:user_id>/', unfollow_user_view, name='unfollow-user'),
]
