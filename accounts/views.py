from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        user = User.objects.get(pk=resp.data['id'])
        token, _ = Token.objects.get_or_create(user=user)
        return Response({**resp.data, 'token': token.key}, status=status.HTTP_201_CREATED)

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        token = resp.data['token']
        user = Token.objects.get(key=token).user
        return Response({'token': token, 'user_id': user.id, 'username': user.username})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    try:
        target = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=404)
    if target == request.user:
        return Response({'detail': 'You cannot follow yourself'}, status=400)
    request.user.following.add(target)
    return Response({'detail': f'Now following {target.username}'})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    try:
        target = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=404)
    request.user.following.remove(target)
    return Response({'detail': f'Unfollowed {target.username}'})
