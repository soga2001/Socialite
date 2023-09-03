import uuid
from django.db import models
# from django.contrib.auth.models import User
from users.models import User
from posts.models import Post

# Create your models here.
class PostViews(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False, related_name='post_viewed')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='user_viewing')
    date_viewed = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'user'], name='unique_views')
        ]
        ordering = ['-date_viewed']
    

