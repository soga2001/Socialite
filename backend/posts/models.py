from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    username = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    user_id = models.IntegerField(default=None)
    img_url = models.URLField(max_length=3000, null=False, blank=False, editable=True)
    caption = models.CharField(max_length=3000, null=True, blank=True, editable=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(default=None, blank=True, null=True) 