from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('', views.posts_list, name="list"),
    path('new-post/', views.post_new, name='new-post'),
    path('my-posts/', views.my_posts, name='my-posts'),
    path('<slug:slug>/', views.post_detail, name='post-detail'),
    path('<slug:slug>/edit/', views.post_edit, name='post-edit'),
    path('<slug:slug>/delete/', views.post_delete, name='post-delete'),
]
