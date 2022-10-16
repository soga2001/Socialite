from django.db import models
from django.contrib.auth.models import User
import os
import uuid
import random

def rename_file(instance, filename):
    file, file_extension = os.path.splitext(filename)
    path = 'media/'
    format = str(instance.user_id) + '-' + str(uuid.uuid4()) + str(file_extension)
    return os.path.join(path, format)

# Create your models here.
class Post(models.Model):
    username = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    user_id = models.IntegerField(default=None)
    img_url = models.FileField(upload_to=rename_file, blank=False, null=False, editable=True)
    caption = models.TextField(max_length=255, null=True, blank=True, editable=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(default=None, blank=True, null=True)


    