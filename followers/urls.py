from django.urls import path
from .views import FollowerList, FollowerDetail

urlpatterns = [
    path('', FollowerList.as_view(), name='follower_list'),
    path('<int:pk>/', FollowerDetail.as_view(), name='follower_detail'),
]