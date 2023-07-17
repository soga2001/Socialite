from django.db import models
from users.models import User
from posts.models import Post

class Comment(models.Model):
    _DATABASE = 'supabase'
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, related_name="user_comments")
    post = models.ForeignKey(Post, blank=False, null=False, on_delete=models.CASCADE, related_name="post_comments")
    comment = models.TextField(max_length=255, null=False, blank=False, editable=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(default=None, blank=True, null=True)

    class Meta:
        ordering = ['-date_posted']