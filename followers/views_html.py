from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Follower
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest

# -----------------------
# List users the current user is following
# -----------------------
@login_required
def following_list_view(request):
    following = Follower.objects.filter(follower=request.user)
    return render(request, "followers/followers_list.html", {"following": following})

# -----------------------
# Follow a user
# -----------------------
@login_required
def follow_user_view(request):
    identifier = request.GET.get('user')  # Could be ID or username
    if not identifier:
        return HttpResponseBadRequest("User identifier required")

    # Try to get by ID first, then by username
    user_to_follow = None
    if identifier.isdigit():
        user_to_follow = User.objects.filter(id=int(identifier)).first()
    if not user_to_follow:
        user_to_follow = User.objects.filter(username=identifier).first()
    if not user_to_follow:
        return HttpResponseBadRequest("User not found")

    if user_to_follow == request.user:
        return HttpResponseBadRequest("Cannot follow yourself")

    if not Follower.objects.filter(follower=request.user, following=user_to_follow).exists():
        Follower.objects.create(follower=request.user, following=user_to_follow)

    return redirect("following-list")

# -----------------------
# Unfollow a user
# -----------------------
@login_required
def unfollow_user_view(request, user_id):
    follow_instance = get_object_or_404(Follower, follower=request.user, following__id=user_id)
    follow_instance.delete()
    return redirect("following-list")
