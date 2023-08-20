from django.db import models
from notifications.base.models import AbstractNotification

class Notification(AbstractNotification):

    class Meta(AbstractNotification.Meta):
        ordering = ['-timestamp']
        abstract = False

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()
import json


from .serializer import NotificationSerializer

@receiver(post_save, sender=Notification)
def notify_handler_post_save(sender, instance, created, **kwargs):
    if created:
        group_name = f'notification_room_{instance.recipient.id}'
        async_to_sync(channel_layer.group_send)(group_name, {
            "type": "post.update",
            "updateType": 'posted',
            "message": json.dumps(NotificationSerializer(instance).data)
        })
    else:
        print('here')

@receiver(post_delete, sender=Notification)
def notify_handler_post_delete(sender, instance, **kwargs):
    group_name = f'notification_room_{instance.recipient.id}'
    async_to_sync(channel_layer.group_send)(group_name, {
        "type": "post.update",
        "updateType": 'deleted',
        "message": json.dumps(NotificationSerializer(instance).data)
    })