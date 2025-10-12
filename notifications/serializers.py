from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField(source='actor.username')
    recipient = serializers.ReadOnlyField(source='recipient.username')
    target_id = serializers.IntegerField(source='object_id', read_only=True)
    target_type = serializers.CharField(source='content_type.model', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target_type', 'target_id', 'timestamp', 'unread']
