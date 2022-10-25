from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

# Create your models here.
class Likes(models.Model):
    likes = models.ManyToManyField(Post, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ManyToManyField(User, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        unique_together = ('likes', 'user')