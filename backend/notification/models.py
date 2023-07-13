from django.db import models
from notifications.base.models import AbstractNotification


class Notification(AbstractNotification):
    link = models.CharField(max_length=200, blank=False, null=False)

    class Meta(AbstractNotification.Meta):
        ordering = ['-timestamp']
        abstract = False