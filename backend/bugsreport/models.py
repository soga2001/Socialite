import uuid
from django.db import models
from users.models import User

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import datetime
from django.forms import ValidationError

# Create your models here.
class BugsReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    bug = models.CharField(max_length=30, null=False, blank=False)
    replication = models.TextField(max_length=255, null=False, blank=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(default=None, blank=True, null=True)
    resolved = models.BooleanField(default=False, blank=False, null=False)
    
    class Meta:
        ordering = ['-date_posted']


    def save(self, *args, **kwargs):
        if len(self.bug) == 0:
            raise ValidationError("Please don't leave the bug field empty!")
        if len(self.replication) == 0:
            raise ValidationError("Please don't leave the replication field empty!")
        super(BugsReport, self).save(*args, **kwargs)

