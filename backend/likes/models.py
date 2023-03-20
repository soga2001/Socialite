from tkinter import CASCADE
from django.db import models
# from django.contrib.auth.models import User
from users.models import User
from posts.models import Post

# Create your models here.
class PostLikes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False, related_name='post_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='user_liked')
    date_liked = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'user'], name='unique_likes')
        ]
        ordering = ['-date_liked']
    

