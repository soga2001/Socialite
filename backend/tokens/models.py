import binascii
import os

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Tokens(models.Model):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='token', on_delete=models.CASCADE)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    expires_at = models.DateTimeField(blank=True, null=True)
    otp = models.PositiveIntegerField(blank=True, null=True)
    type_choices = [
        ('email_verification', 'email_verification'),
        ('password_reset', 'password_reset'),

    ]

    type = models.CharField(max_length=20, choices=type_choices, default='email_verification')

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")
        constraints = [
            models.UniqueConstraint(fields=['user', 'type'], name='unique_token')
        ]

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)  # Call super().save without returning

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
