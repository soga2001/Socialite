from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.search import SearchVector
from django.db import models
from django.dispatch import receiver
import os, uuid
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
# import Refreshtoken from simplejwt
from rest_framework_simplejwt.tokens import RefreshToken
from backend.encryption import *


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
    email_verified = models.BooleanField(blank=False, null=False, default=False, editable=True)
    emailed_user = models.BooleanField(blank=False, null=False, default=False, editable=True)

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
    


@receiver(post_save, sender=User)
def send_user_verification(sender, instance, created, **kwargs):
    if created:
        subject = 'Verify Your Email'
        token = RefreshToken.for_user(instance).access_token
        html_message = render_to_string('emails/verify_email.html', {'verification_link': settings.EMAIL_VERIFY_URL + str(token)})
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER  # Change this to your email
        recipient_list = [instance.email]
        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
        instance.emailed_user = True