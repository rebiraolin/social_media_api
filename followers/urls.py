from django.urls import path
from .views import FollowingListCreateView, UnfollowView  # API views
from .views_html import following_list_view, follow_user_view, unfollow_user_view  # HTML views

urlpatterns = [
    # -----------------------
    # API endpoints
    # -----------------------
    path('api/', FollowingListCreateView.as_view(), name='following-list-create-api'),
    path('api/unfollow/<int:following_id>/', UnfollowView.as_view(), name='unfollow-user-api'),

    # -----------------------
    # HTML pages
    # -----------------------
    path('', following_list_view, name='following-list'),
    path('follow/<int:user_id>/', follow_user_view, name='follow-user'),
    path('unfollow/<int:user_id>/', unfollow_user_view, name='unfollow-user'),
]
