from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

# For notifications
from notifications.models import Notification

CustomUser = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        user = CustomUser.objects.get(pk=resp.data['id'])
        token, _ = Token.objects.get_or_create(user=user)
        return Response({**resp.data, 'token': token.key}, status=status.HTTP_201_CREATED)

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        token = resp.data['token']
        user = Token.objects.get(key=token).user
        return Response({'token': token, 'user_id': user.id, 'username': user.username})

class FollowUserView(generics.GenericAPIView):
    """
    POST to follow a user: /api/accounts/follow/<user_id>/
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id, *args, **kwargs):
        target = get_object_or_404(self.get_queryset(), pk=user_id)
        if target == request.user:
            return Response({'detail': "You can't follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.following.add(target)
        # create notification for the followed user
        if target != request.user:
            Notification.objects.create(
                recipient=target,
                actor=request.user,
                verb='started following you',
                content_type=None,
                object_id=request.user.id
            )
        return Response({'detail': f'You are now following {target.username}'}, status=status.HTTP_200_OK)

class UnfollowUserView(generics.GenericAPIView):
    """
    POST to unfollow a user: /api/accounts/unfollow/<user_id>/
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id, *args, **kwargs):
        target = get_object_or_404(self.get_queryset(), pk=user_id)
        request.user.following.remove(target)
        return Response({'detail': f'You have unfollowed {target.username}'}, status=status.HTTP_200_OK)
