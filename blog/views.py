from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.

def posts_list(request):
    posts=Post.objects.all().order_by('-date')
    return render(request, 'blog/posts_list.html', {'posts':posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required(login_url="/accounts/login/")
def post_new(request):
    return render(request, "blog/post_new.html")