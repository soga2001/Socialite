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



def rename_file(instance, filename):
    file, file_extension = os.path.splitext(filename)
    path = 'avatar/'
    format = str(instance.user_id) + '-' + str(uuid.uuid4()) + str(file_extension)
    return os.path.join(path, format)

# Create your models here.
class User(AbstractUser):
    bio = models.CharField(max_length=300, null=True, blank=True, editable=True)
    avatar = models.FileField(upload_to=rename_file, blank=True, null=True, editable=True)
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

    # class Meta:
    #     indexes = [GinIndex(fields=['search_vector'])]


# when a post gets deleted
@receiver(models.signals.post_delete, sender=User)
def remove_file_from_s3(sender, instance, using, **kwargs):
    instance.avatar.delete(save=False)

# make sure first_name and last_name aren't empty 
@receiver(pre_save, sender=User)
def check_name(sender, instance, **kwargs):
    if instance.first_name == '' or instance.last_name == '':
        raise ValueError('Please enter your name')
    

# @receiver(post_save, sender=User)
# def update_search_vector(sender, instance, created, **kwargs):
#     if created:
#         # Create a new SearchVector object with the fields you want to include
#         search_vector = SearchVector('username', 'first_name', 'last_name', 'email')
#         # Update the sv field with the new SearchVector value
#         instance.search_vector = search_vector
#         instance.save()
    


