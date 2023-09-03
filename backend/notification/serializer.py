from rest_framework import serializers
from .models import Notification
# import UserSerializer
from users.serializer import *
import json

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer()
    data = serializers.SerializerMethodField()
    id = serializers.UUIDField()
    recipient = serializers.UUIDField()
    target = serializers.UUIDField()
    action_object = serializers.UUIDField()

    
    class Meta:
        model = Notification
        fields = '__all__'

    def get_data(self, obj):
        if(isinstance(obj.data, str)):
            return json.loads(obj.data)
        return obj.data