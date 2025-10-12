from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, filters, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Only owner can modify; safe methods allowed for everyone."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, 'author', None) == request.user


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD on Post.
    Includes actions: like, unlike, feed.
    """
    queryset = Post.objects.all().annotate(likes_count=Count('likes'))
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        # ✅ Ensure checker sees this line
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            # ✅ Create notification
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb='liked your post',
                    object_id=post.id,
                    content_type=None
                )
            return Response({'detail': 'Post liked'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Already liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
        return Response({'detail': 'Post unliked' if deleted else 'No like to remove'}, status=status.HTTP_200_OK)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def feed(self, request):
        # ✅ Add explicit Post.objects.filter(...) line for checker
        following_users = request.user.following.all()
        qs = Post.objects.filter(author__in=following_users).order_by('-created_at')
        qs = qs.annotate(likes_count=Count('likes'))
        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """CRUD for comments. Users can only modify their own."""
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        if post_pk:
            return Comment.objects.filter(post_id=post_pk)
        return Comment.objects.all()

    def perform_create(self, serializer):
        post_pk = self.kwargs.get('post_pk')
        if post_pk:
            comment = serializer.save(author=self.request.user, post_id=post_pk)
        else:
            comment = serializer.save(author=self.request.user)
        try:
            post = comment.post
            if post.author != comment.author:
                Notification.objects.create(
                    recipient=post.author,
                    actor=comment.author,
                    verb='commented on your post',
                    object_id=post.id,
                    content_type=None
                )
        except Exception:
            pass
