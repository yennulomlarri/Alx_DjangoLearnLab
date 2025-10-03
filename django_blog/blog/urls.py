from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    # Home and authentication
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # USE CUSTOM LOGOUT VIEW INSTEAD
    path('logout/', views.custom_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Post URLs
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    
    # Comment URLs
    path('post/<int:pk>/comment/', views.add_comment, name='add-comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete-comment'),
    
    # Search and Tag URLs
    path('search/', views.search_posts, name='search'),
    path('tag/<slug:tag_slug>/', views.posts_by_tag, name='posts-by-tag'),
]