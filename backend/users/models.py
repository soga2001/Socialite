from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.search import SearchVector
from django.db import models
import os, uuid
from django.core.mail import send_mail
from django.forms import ValidationError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
# import Refreshtoken from simplejwt
from rest_framework_simplejwt.tokens import RefreshToken
from backend.encryption import *
from backend.encryption import AESCipher
from PIL import Image
from io import BytesIO
from django.core.files import File

# from rest_framework.authtoken.models import Token
from tokens.models import Tokens
import datetime
from phone_field import PhoneField


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

def compress(image, height, width):
    im = Image.open(image)
    im_io = BytesIO()
    im.resize((width, height))
    im.save(im_io, 'JPEG', quality=60) 

    new_image = File(im_io, name=image.name)
    return new_image

# Create your models here.
class User(AbstractUser):
    bio = models.CharField(max_length=160, null=True, blank=True, editable=True)
    avatar = models.FileField(upload_to=rename_avatar, blank=True, null=True, editable=True)
    banner = models.FileField(upload_to=rename_banner, blank=True, null=True, editable=True)
    email_verified = models.BooleanField(blank=False, null=False, default=False, editable=True)
    emailed_user = models.BooleanField(blank=False, null=False, default=False, editable=True)
    private = models.BooleanField(blank=False, null=False, default=False, editable=True)
    verified = models.BooleanField(blank=False, null=False, default=False, editable=True)
    is_admin = models.BooleanField(blank=False, null=False, default=False, editable=True)
    link = models.URLField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    full_name = models.CharField(max_length=30, blank=False, null=False, default='Suyogya Poudel')
    dob = models.DateTimeField(default=None, blank=True, null=True)
    phone = PhoneField(blank=True, help_text='Contact phone number')


    def save(self, *args, **kwargs):
        # if self.dob and self.dob > datetime.datetime.now():
        #     raise ValidationError("The date cannot be in the future!")
        # # date cannot be passed 100 years ago
        # if self.dob and self.dob < datetime.datetime.now() - datetime.timedelta(days=365*120):
        #     raise ValidationError("The date cannot be more than 100 years ago!")
        # if self.dob and self.dob > datetime.datetime.now() - datetime.timedelta(days=365*13):
        #     raise ValidationError("The date cannot be less than 13 years ago!")
        if(len(self.full_name) == 0):
            raise ValidationError("You cannot leave the name field empty")
        
 
        super(User, self).save(*args, **kwargs)

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


@receiver(models.signals.pre_delete, sender=User)
def auto_delete_notification(sender, instance, **kwargs):
    try:
        instance.notifications.filter(actactor_object_idor=instance.id).delete()
    except Exception as e:
        print(e)
        pass

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

    


# # make sure first_name and last_name aren't empty 
# @receiver(pre_save, sender=User)
# def check_name(sender, instance, **kwargs):
#     if instance.first_name == '' or instance.last_name == '':
#         raise ValueError('Please enter your name')
    


@receiver(post_save, sender=User)
def send_user_verification(sender, instance, created=False, **kwargs):
    if created:
        subject = 'Verify Your Email'
        expires_at = datetime.datetime.now() + datetime.timedelta(days=1)
        token = Tokens.objects.create(user=instance, expires_at=expires_at)
        html_message = render_to_string('emails/verify_email.html', {'verification_link': settings.EMAIL_VERIFY_URL + token.key, 'full_name': instance.full_name})
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER  # Change this to your email
        recipient_list = [instance.email]
        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
        instance.emailed_user = True