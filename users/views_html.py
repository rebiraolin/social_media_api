from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, LoginForm, UserProfileUpdateForm
from .models import Profile
from posts.models import Post
from followers.models import Follower

def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user)
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, "users/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("post_list")
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def profile_view(request, username=None):
    if username:
        user_to_view = get_object_or_404(User, username=username)
    else:
        user_to_view = request.user

    is_following = False
    if request.user != user_to_view:
        is_following = Follower.objects.filter(
            follower=request.user,
            following=user_to_view
        ).exists()

    posts = Post.objects.filter(user=user_to_view).order_by('-timestamp')

    context = {
        'user_profile': user_to_view,
        'is_following': is_following,
        'posts': posts,
    }
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("user-profile", username=request.user.username)
    else:
        form = UserProfileUpdateForm(instance=profile)
    return render(request, "users/edit_profile.html", {"form": form, "profile": profile})

@login_required
def remove_profile_picture(request):
    profile = get_object_or_404(Profile, user=request.user)
    if profile.profile_picture:
        profile.profile_picture.delete(save=False)
        profile.profile_picture = None
        profile.save()
    return redirect('edit_profile')
