# import serializer
from rest_framework import serializers

from .models import BugsReport
from users.serializer import *

class BugsReportSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    id = serializers.UUIDField()
    
    class Meta:
        model = BugsReport
        fields = '__all__'
