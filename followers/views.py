from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Follower
from .serializers import FollowerSerializer


class FollowerListCreateView(generics.ListCreateAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Prevent a user from following themselves
        if self.request.user == serializer.validated_data['following']:
            raise serializers.ValidationError("You cannot follow yourself.")
        serializer.save(follower=self.request.user)

    def get_queryset(self):
        # Only show the followers of the currently authenticated user
        return Follower.objects.filter(following=self.request.user)


class FollowerDestroyView(generics.DestroyAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure only the follower can unfollow
        return self.queryset.filter(follower=self.request.user)