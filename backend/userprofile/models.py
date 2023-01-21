from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os, uuid

def rename_file(instance, filename):
    file, file_extension = os.path.splitext(filename)
    path = 'avatar/'
    format = str(instance.user_id) + '-' + str(uuid.uuid4()) + str(file_extension)
    return os.path.join(path, format)


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, primary_key=True)
    bio = models.CharField(max_length=300, null=True, blank=True, editable=True)
    avatar = models.FileField(upload_to=rename_file, blank=True, null=True, editable=True)


# when a post gets deleted
@receiver(models.signals.post_delete, sender=UserProfile)
def remove_file_from_s3(sender, instance, using, **kwargs):
    instance.avatar.delete(save=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html