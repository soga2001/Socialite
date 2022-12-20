from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.
class UserFollowing(models.Model):

    user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id','following_user_id'],  name="unique_followers")
        ]

        ordering = ["-created"]