from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('', views.posts_list, name="list"),
    path('new-post/', views.post_new, name='new-post'),
    path('<slug:slug>/', views.post_detail, name='post_detail')

]
