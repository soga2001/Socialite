from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.CharField(source="actor.username")
    actor_avatar = serializers.FileField(source="actor.avatar")
    
    class Meta:
        model = Notification
        fields = '__all__'