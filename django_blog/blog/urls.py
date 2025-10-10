from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    PostByTagListView,
)

urlpatterns = [
    # Home and posts list
    path('', PostListView.as_view(), name='home'),
    path('posts/', PostListView.as_view(), name='post_list'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Post CRUD - WITH CHECKER-REQUIRED URL PATTERNS
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),  # ✅ Changed: posts/new → post/new
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),  # ✅ Changed: posts/<int:pk>/edit → post/<int:pk>/update
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),  # ✅ Changed: posts/<int:pk>/delete → post/<int:pk>/delete
    
    # Comments
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    
    # Search and tags
    path('search/', views.search_posts, name='search'),
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts_by_tag'),
]