from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Follower

@login_required
def following_list_view(request):
    query = request.GET.get('q')
    users_found = None
    if query:
        users_found = User.objects.filter(username__icontains=query).exclude(id=request.user.id)

    if request.method == 'POST':
        username_to_follow = request.POST.get('username_to_follow')
        if username_to_follow:
            try:
                user_to_follow = User.objects.get(username=username_to_follow)
                if request.user == user_to_follow:
                    messages.error(request, "You cannot follow yourself.")
                else:
                    Follower.objects.get_or_create(follower=request.user, following=user_to_follow)
                    messages.success(request, f"You are now following {username_to_follow}.")
            except User.DoesNotExist:
                messages.error(request, f"User '{username_to_follow}' does not exist.")
        return redirect('following-list')

    following = Follower.objects.filter(follower=request.user)
    return render(request, "followers/followers_list.html", {"following": following, "users_found": users_found})

@login_required
def unfollow_user_view(request, user_id):
    follow_instance = get_object_or_404(Follower, follower=request.user, following__id=user_id)
    follow_instance.delete()
    return redirect("following-list")
