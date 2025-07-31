from django.shortcuts import render, redirect
from .models import Post
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms

# Create your views here.

def posts_list(request):
    posts = Post.objects.all().order_by('-date')
    tag = request.GET.get('tag')
    if tag:
        posts = posts.filter(tags__name__iexact=tag)

    return render(request, 'blog/posts_list.html', {
        'posts': posts,
        'active_tag': tag,
        'request': request
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all().order_by('-created_at')

    if request.method == "POST":
        form = forms.CreateComment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('blog:post-detail', slug=slug)
    else:
        form = forms.CreateComment()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })

@login_required(login_url="/accounts/login/")
def post_new(request):
    if request.method == "POST":
        form = forms.CreatePost(request.POST) #add request.FILES if images are included
        if form.is_valid():
            form.save(user=request.user)
            return redirect('blog:list')
    else:
        form = forms.CreatePost()
    return render(request, "blog/post_new.html", {'form': form})