from django.shortcuts import render, redirect
from .models import Post
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms
from django.core.paginator import Paginator
import markdown
from django.utils.safestring import mark_safe
from .utils import get_markdown_paragraph_preview

# Create your views here.

def posts_list(request):
    posts = Post.objects.all().order_by('-date')
    tag = request.GET.get('tag')
    if tag:
        posts = posts.filter(tags__name__iexact=tag)
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    for post in page_obj:
        preview_length = 150 # Adjust as needed
        post.preview = mark_safe(get_markdown_paragraph_preview(post.body, preview_length))

    query_dict = request.GET.copy()
    query_dict.pop('page', None)
    base_query = query_dict.urlencode()

    return render(request, 'blog/posts_list.html', {
        'posts': page_obj,
        'page_obj': page_obj,
        'active_tag': tag,
        'base_query': base_query,
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    # Render Markdown to HTML
    post_html = mark_safe(markdown.markdown(post.body))

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
        'post_html': post_html,
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

@login_required(login_url="/accounts/login/")
def my_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-date')
    tag = request.GET.get('tag')
    if tag:
        posts = posts.filter(tags__name__iexact=tag)
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for post in page_obj:
        preview_length = 150 # Adjust as needed
        post.preview = mark_safe(get_markdown_paragraph_preview(post.body, preview_length))
    
    query_dict = request.GET.copy()
    query_dict.pop('page', None)
    base_query = query_dict.urlencode()

    return render(request, 'blog/my_posts.html', {
        'posts': page_obj,
        'page_obj': page_obj,
        'active_tag': tag,
        'base_query': base_query,
    })

@login_required(login_url="/accounts/login/")
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = forms.CreatePost(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post-detail', slug=slug)
    else:
        form = forms.CreatePost(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('blog:my-posts') 

