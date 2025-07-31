from django.shortcuts import render, redirect
from .models import Post
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms

# Create your views here.

def posts_list(request):
    posts=Post.objects.all().order_by('-date')
    return render(request, 'blog/posts_list.html', {'posts':posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

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