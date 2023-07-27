from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import PostLikes

from users.serializer import UserSerializer

class PostLikesSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True, default=UserSerializer())
    user = serializers.SerializerMethodField()

    class Meta:
        model = PostLikes
        fields = '__all__'

    # def get_user(self, obj):
    #     return obj.user

    def get_user(self, obj):
        # Get the user instance from the UserFollowing object
        user_instance = obj.user
        
        # Serialize the user data using the UserSerializer
        user_serializer = UserSerializer(user_instance, context=self.context)
        
        # Return the serialized user data
        return user_serializer.data

    
