from django.db import models
# from django.contrib.auth.models import User
from users.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from notifications.signals import notify
from notification.models import Notification

# Create your models here.
class UserFollowing(models.Model):
    followed_user = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    followed_date = models.DateTimeField(auto_now_add=True, db_index=True)
    notification = models.BooleanField(blank=False, null=False, default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['followed_user','following_user'],  name="unique_followers")
        ]

        ordering = ["-followed_date"]


# post save
@receiver(post_save, sender=UserFollowing)
def create_notification(sender, instance, created, **kwargs):
    if created:
        notify.send(instance.following_user, recipient=instance.followed_user, verb='followed', action_object=instance, description=f'{instance.following_user.username} followed you', target=instance.followed_user)


# post delete
@receiver(post_delete, sender=UserFollowing)
def delete_notification(sender, instance, **kwargs):
    try:
        Notification.objects.filter(actor_object_id=instance.following_user.id, recipient=instance.followed_user, verb='followed').delete()
    except Exception as e:
        print(e)
        pass
    # notify.send(instance.following_user, recipient=instance.followed_user, verb='unfollowed you', action_object=instance, description=f'{instance.following_user.username} unfollowed you', target=instance.followed_user)