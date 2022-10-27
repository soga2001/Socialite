from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

# Create your models here.
class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        unique_together = ('post', 'user')