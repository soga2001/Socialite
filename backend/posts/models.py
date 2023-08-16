from calendar import c
from socket import send_fds
from django.db import models
# from django.contrib.auth.models import User
from users.models import User
from django.db.models.signals import post_delete
import os
import uuid

from django.dispatch import receiver

def rename_file(instance, filename):
    file, file_extension = os.path.splitext(filename)
    path = 'media/posts/'
    format = str(instance.user_id) + '-' + str(uuid.uuid4()) + str(file_extension)
    return os.path.join(path, format)

# Create your models here.
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, related_name="user_posted")
    # user_id = models.IntegerField(default=None)
    img_url = models.FileField(upload_to=rename_file, blank=False, null=False, editable=True)
    caption = models.TextField(max_length=255, null=True, blank=True, editable=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(default=None, blank=True, null=True)
    
    class Meta:
        ordering = ['-date_posted']


# when a post gets deleted
@receiver(models.signals.post_delete, sender=Post)
def remove_file_from_s3(sender, instance, using, **kwargs):
    instance.img_url.delete(save=False)


    