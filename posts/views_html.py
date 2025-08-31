# posts/views_html.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

@login_required
def post_list_view(request):
    # Change 'created_at' to 'timestamp'
    posts = Post.objects.all().order_by('-timestamp')
    return render(request, "posts/post_list.html", {"posts": posts})

@login_required
def my_posts_view(request):
    # Change 'created_at' to 'timestamp'
    posts = Post.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, "posts/my_posts.html", {"posts": posts})

@login_required
def create_post_view(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("post_list")
    else:
        form = PostForm()
    return render(request, "posts/create_post.html", {"form": form})

@login_required
def edit_post_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("my_posts")
    else:
        form = PostForm(instance=post)
    return render(request, "posts/edit_post.html", {"form": form, "post": post})