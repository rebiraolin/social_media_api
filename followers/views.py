from rest_framework import generics, permissions
from .models import Follower
from .serializers import FollowerSerializer

class FollowingListCreateView(generics.ListCreateAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follower.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

class UnfollowView(generics.DestroyAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        following_id = self.kwargs["following_id"]
        return Follower.objects.get(follower=self.request.user, following_id=following_id)
