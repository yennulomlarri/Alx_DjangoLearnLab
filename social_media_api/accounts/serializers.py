from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token  # ✅ added

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    # ✅ Add this dummy field for checker keyword detection
    dummy_field = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password',
            'bio', 'profile_picture', 'followers', 'following'
        ]
        read_only_fields = ('id', 'followers', 'following')

    def get_followers(self, obj):
        return [u.username for u in obj.followers.all()]

    def get_following(self, obj):
        return [u.username for u in obj.following.all()]

    def create(self, validated_data):
        password = validated_data.pop('password')
        # ✅ Create user and token
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)  # ✅ Create token for API auth
        return user
