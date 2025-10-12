from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like, Comment
from notifications.models import Notification

@receiver(post_save, sender=Like)
def notify_like(sender, instance, created, **kwargs):
    if created and instance.user != instance.post.author:
        Notification.objects.create(
            recipient=instance.post.author,
            actor=instance.user,
            verb='liked your post',
            target=instance.post
        )

@receiver(post_save, sender=Comment)
def notify_comment(sender, instance, created, **kwargs):
    if created and instance.author != instance.post.author:
        Notification.objects.create(
            recipient=instance.post.author,
            actor=instance.author,
            verb='commented on your post',
            target=instance.post
        )
