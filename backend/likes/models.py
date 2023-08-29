from tkinter import CASCADE
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
        link = '{}/spill/{}'.format(instance.post.user.username, instance.post.id)
        notify.send(instance.user, recipient=instance.post.user, verb='liked', action_object=instance, description=f'{instance.user.username} liked your post', target=instance.post, url=link, text=instance.post.caption)



# post delete
@receiver(post_delete, sender=PostLikes)
def delete_notification(sender, instance, **kwargs):
    try:
        if(instance.post.user != instance.user):
            Notification.objects.filter(actor_object_id=instance.user.id, recipient=instance.post.user, verb='liked').delete()
    except Exception as e:
        print(e)
        pass
    # notify.send(instance.user, recipient=instance.post.user, verb='unliked your post', action_object=instance, description=f'{instance.user.username} unliked your post', target=instance.post)
    

