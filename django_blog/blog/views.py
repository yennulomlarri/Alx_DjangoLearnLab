from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q  
from taggit.models import Tag  
from .models import Post, Comment
from .forms import UserRegisterForm, PostForm, CommentForm, ProfileForm  # ✅ Added ProfileForm import

def home(request):
    posts = Post.objects.all().order_by('-published_date')[:3] 
    return render(request, 'blog/home.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

def custom_logout(request):
    auth_logout(request)
    messages.success(request, 'You have been successfully logged out!')
    return redirect('home')

# ✅ FIXED PROFILE VIEW TO HANDLE PROFILE EDIT
@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'registration/profile.html', {'form': form})

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created_at')
        context['comment_form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated!')
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('post-detail', pk=post.pk)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author == request.user:
        comment.delete()
        messages.success(request, 'Your comment has been deleted!')
    return redirect('post-detail', pk=comment.post.pk)

def search_posts(request):
    query = request.GET.get('q')
    tag_name = request.GET.get('tag')
    
    posts = Post.objects.all()
    
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    if tag_name:
        posts = posts.filter(tags__name__in=[tag_name])
        try:
            tag_name = Tag.objects.get(name=tag_name)
        except Tag.DoesNotExist:
            tag_name = None
    
    context = {
        'posts': posts,
        'query': query,
        'tag': tag_name,
        'search_performed': bool(query or tag_name)
    }
    return render(request, 'blog/search_results.html', context)

def posts_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags__in=[tag])
    
    context = {
        'posts': posts,
        'tag': tag,
    }
    return render(request, 'blog/posts_by_tag.html', context)
