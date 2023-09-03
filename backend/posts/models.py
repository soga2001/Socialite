from django.db import models
# from django.contrib.auth.models import User
from users.models import User
from django.db.models.signals import post_delete, post_save
import os
import uuid
from notifications.signals import notify

from django.dispatch import receiver

def rename_file(instance, filename):
    print('here')
    file, file_extension = os.path.splitext(filename)
    path = 'media/{}/posts'.format(instance.user_id)
    format = str(uuid.uuid4()) + str(file_extension)
    return os.path.join(path, format)

# Create your models here.
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, related_name="user_posted")
    img_url = models.FileField(upload_to=rename_file, blank=True, null=True, editable=True)
    caption = models.TextField(max_length=255, null=True, blank=True, editable=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(default=None, blank=True, null=True)
    
    class Meta:
        ordering = ['-date_posted']
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_either_img_url_or_caption",
                check=(
                    models.Q(img_url__isnull=False) | models.Q(caption__isnull=False)
                ),
            )
        ]


# when a post gets deleted
@receiver(post_delete, sender=Post)
def remove_file_from_s3(sender, instance, using, **kwargs):
    instance.img_url.delete(save=False)


@receiver(post_save, sender=Post)
def update_post(sender, instance, created, **kwargs):

    link = "{}/spill/{}".format(instance.user.username, instance.id)

    followers = instance.user.followers.filter(notification=True)
    follower_ids = followers.values_list('following_user')
    
    batch_size = 100
    
    for start in range(0, len(follower_ids), batch_size):
        batch_ids = follower_ids[start:start+batch_size]
        batch_recipients = User.objects.filter(id__in=batch_ids)
        
        notify.send(
            instance.user,
            recipient=batch_recipients,
            verb='spilled',
            action_object=instance,
            target=instance,
            description="spilled a tea",
            url=link,
            text=instance.caption
        )


    