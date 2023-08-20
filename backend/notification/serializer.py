from rest_framework import serializers
from .models import Notification
# import UserSerializer
from users.serializer import UserSerializer
import json

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer()
    data = serializers.JSONField()
    
    
    class Meta:
        model = Notification
        fields = '__all__'
