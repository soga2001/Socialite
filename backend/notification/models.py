from django.db import models
from notifications.base.models import AbstractNotification
from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import Post
from following.models import UserFollowing



class Notification(AbstractNotification):
    _DATABASE = 'supabase'
    link = models.CharField(max_length=200, blank=False, null=False)
    # followed = models.ForeignKey(UserFollowing, blank=True, null=True, related_name='followed')


    class Meta(AbstractNotification.Meta):
        ordering = ['-timestamp']
        abstract = False



# post_save signal
@receiver(post_save, sender=Notification)
def notify_handler(sender, instance, created, **kwargs):
    # if created:
    #     verb = instance.verb
    #     description = instance.description
    #     notify.send(instance.actor, recipient=instance.recipient, verb=verb, description=description, link=instance.link)
    print(instance, sender)