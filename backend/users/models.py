from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(pre_save, sender=User)
def check_name(sender, instance, **kwargs):
    if instance.first_name == '' or instance.last_name == '':
        raise ValueError('Please enter your name')
    if instance.username == '':
        raise ValueError('Please enter your username')
    if instance.email == '':
        raise ValueError('Please enter your email')
    if instance.password == '':
        raise ValueError('Please enter your password')
    # if instance.confirm_password == '':
    #     raise ValueError('Please enter your confirm password')
    # if instance.password != instance.confirm_password:
    #     raise ValueError('Password and confirm password must match')