from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    avatar = models.URLField(max_length=500, blank=True, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html