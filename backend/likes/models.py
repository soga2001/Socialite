import uuid
from django.db import models
# from django.contrib.auth.models import User
from users.models import User
from posts.models import Post

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from notifications.signals import notify
from notification.models import Notification

# Create your models here.
class PostLikes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False, related_name='post_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='user_liked')
    date_liked = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'user'], name='unique_likes')
        ]
        ordering = ['-date_liked']



# post save
@receiver(post_save, sender=PostLikes)
def create_notification(sender, instance, created, **kwargs):
    if created and instance.post.user != instance.user:
        try:
            link = '{}/spill/{}'.format(instance.post.user.username, instance.post.id)
            text = 'Image' if not instance.post.caption else instance.post.caption
            notify.send(instance.user, recipient=instance.post.user, verb='liked', action_object=instance, description='liked your post', target=instance.post, url=link, text=text)
        except Exception as e:
            print('post_save',e)
            pass



# # post delete
@receiver(post_delete, sender=PostLikes)
def delete_notification(sender, instance, **kwargs):
    try:
        user_id = instance.user.id
        post_user_id = instance.post.user.id

        if user_id is not None and post_user_id is not None and user_id != post_user_id:
            notifications_to_delete = Notification.objects.filter(
                actor_object_id=str(user_id),
                recipient=str(post_user_id),
                verb='liked'
            )
            notifications_to_delete.delete()
    except Exception as e:
        pass
    # notify.send(instance.user, recipient=instance.post.user, verb='unliked your post', action_object=instance, description=f'{instance.user.username} unliked your post', target=instance.post)
    

