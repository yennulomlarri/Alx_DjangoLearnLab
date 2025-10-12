from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

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
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
