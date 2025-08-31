# followers/views.py

from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from .models import Follower
from .serializers import FollowerSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class FollowingListCreateView(generics.ListCreateAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # The serializer will validate the 'following' user ID
        following_user = serializer.validated_data.get('following')

        # Prevent a user from following themselves
        if self.request.user == following_user:
            raise serializers.ValidationError({"detail": "You cannot follow yourself."})

        # Check for duplicate follow relationships
        if Follower.objects.filter(follower=self.request.user, following=following_user).exists():
            raise serializers.ValidationError({"detail": "You are already following this user."})

        serializer.save(follower=self.request.user)

    def get_queryset(self):
        # List users the authenticated user is following
        return Follower.objects.filter(follower=self.request.user)


class UnfollowView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # We get the user ID to unfollow from the URL
        following_id = self.kwargs.get('following_id')

        # Look up the follow relationship for the current user and the specified user
        follow_instance = get_object_or_404(
            Follower,
            follower=self.request.user,
            following__id=following_id
        )
        return follow_instance