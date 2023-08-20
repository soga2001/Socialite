from django.apps import AppConfig


class NotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notification'


    # def ready(self):
    #     super(NotificationConfig, self).ready()
    #     # this is for backwards compatibility
    #     import notifications.signals
    #     notifications.notify = notifications.signals.notify
