from django.db.models.signals import pre_save
from django.dispatch import receiver
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.search import SearchVector
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import os, uuid



def rename_avatar(instance, filename):
    file, file_extension = os.path.splitext(filename)
    path = 'media/avatar/'
    format = str(instance.id) + '-' + str(uuid.uuid4()) + str(file_extension)
    return os.path.join(path, format)

def rename_banner(instance, filename):
    file, file_extension = os.path.splitext(filename)
    path = 'media/banner/'
    format = str(instance.id) + '-' + str(uuid.uuid4()) + str(file_extension)
    return os.path.join(path, format)

# Create your models here.
class User(AbstractUser):
    bio = models.CharField(max_length=300, null=True, blank=True, editable=True)
    avatar = models.FileField(upload_to=rename_avatar, blank=True, null=True, editable=True)
    banner = models.FileField(upload_to=rename_banner, blank=True, null=True, editable=True)
    # search_vector = SearchVectorField(null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='user_groups', 
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='user_permissions', 
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )


# when a post gets deleted
@receiver(models.signals.post_delete, sender=User)
def remove_file_from_s3(sender, instance, using, **kwargs):
    instance.avatar.delete(save=False)
    instance.banner.delete(save=False)

@receiver(pre_save, sender=User)
def auto_delete_files_on_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = User.objects.get(pk=instance.pk)
            
            if old_instance.avatar and instance.avatar != old_instance.avatar:
                old_instance.avatar.delete(save=False)
            
            if old_instance.banner and instance.banner != old_instance.banner:
                old_instance.banner.delete(save=False)
        
        except User.DoesNotExist:
            pass

    


# make sure first_name and last_name aren't empty 
@receiver(pre_save, sender=User)
def check_name(sender, instance, **kwargs):
    if instance.first_name == '' or instance.last_name == '':
        raise ValueError('Please enter your name')
    

