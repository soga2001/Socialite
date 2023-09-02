from rest_framework import serializers
from .models import Notification
# import UserSerializer
from users.serializer import *

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer()
    data = serializers.JSONField()
    id = serializers.UUIDField()
    recipient = serializers.UUIDField()
    target = serializers.UUIDField()
    action_object = serializers.UUIDField()

    
    class Meta:
        model = Notification
        fields = '__all__'
