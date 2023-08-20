from rest_framework import serializers
# from django.contrib.auth.models import User
from following.models import UserFollowing

from users.serializer import UserSerializer

class UserFollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFollowing
        fields = '__all__'

    