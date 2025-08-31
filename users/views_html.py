# users/views_html.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, LoginForm, UserProfileUpdateForm # Only import the new form
from .models import Profile

# -----------------------
# Registration View
# -----------------------
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

# -----------------------
# Login View
# -----------------------
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

# -----------------------
# Logout View
# -----------------------
def logout_view(request):
    logout(request)
    return redirect("login")

# -----------------------
# Profile View (Display only)
# -----------------------
@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, "users/profile.html", {"profile": profile})

# -----------------------
# Edit Profile View (Handles the form)
# -----------------------
@login_required
def edit_profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("user-profile")
    else:
        form = UserProfileUpdateForm(instance=profile)
    return render(request, "users/edit_profile.html", {"form": form, "profile": profile})

@login_required
def remove_profile_picture(request):
    profile = get_object_or_404(Profile, user=request.user)
    if profile.profile_picture:
        profile.profile_picture.delete(save=False) # Delete the file from the filesystem
        profile.profile_picture = None
        profile.save()
    return redirect('edit_profile')