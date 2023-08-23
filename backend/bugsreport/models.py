from django.db import models
from users.models import User

# Create your models here.
class BugsReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    bug = models.CharField(max_length=30, null=False, blank=False)
    replication = models.TextField(max_length=255, null=False, blank=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(default=None, blank=True, null=True)
    resolved = models.BooleanField(default=False, blank=False, null=False)
    
    class Meta:
        ordering = ['-date_posted']