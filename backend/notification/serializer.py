from rest_framework import serializers
from .models import Notification
# import UserSerializer
from users.serializer import *
import json

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer()
    data = serializers.JSONField()
    
    class Meta:
        model = Notification
        fields = '__all__'

    # def get_actor(self, obj):
    #     if(self.context):
    #         return BasicUserSerializer(obj.actor, context=self.context ).data
    #     return BasicUserSerializer(obj.actor).data