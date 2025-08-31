from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import Post
from .serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly
from followers.models import Follower

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['timestamp', 'user']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['timestamp', 'user']
    search_fields = ['content', 'user__username']

    def get_queryset(self):
        user = self.request.user
        following_users = Follower.objects.filter(follower=user).values_list('following_id', flat=True)
        following_and_own_posts = list(following_users) + [user.id]
        return Post.objects.filter(user_id__in=following_and_own_posts)
