# posts/views_html.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.db.models import Q

@login_required
def post_list_view(request):
    posts = Post.objects.all().order_by('-timestamp')
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(content__icontains=query) |
            Q(user__username__icontains=query)
        )
    return render(request, "posts/post_list.html", {"posts": posts})

@login_required
def my_posts_view(request):
    my_posts = Post.objects.filter(user=request.user).order_by('-timestamp')
    context = {
        'my_posts': my_posts,
    }
    return render(request, "posts/my_posts.html", context)

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

@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Check if the logged-in user is the owner of the post
    if request.user == post.user:
        post.delete()
    return redirect('my_posts')