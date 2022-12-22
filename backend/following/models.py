from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.
class UserFollowing(models.Model):
    followed_user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    followed_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['followed_user','following_user'],  name="unique_followers")
        ]

        ordering = ["-followed_date"]