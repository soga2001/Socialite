from rest_framework import serializers
from django.contrib.auth.models import User
from userprofile.serializer import UserProfileSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    profile = UserProfileSerializer(read_only=True)