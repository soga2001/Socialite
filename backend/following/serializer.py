from rest_framework import serializers
# from django.contrib.auth.models import User
from following.models import UserFollowing

from users.serializer import UserSerializer

class UserFollowingSerializer(serializers.ModelSerializer):
    followed_user = UserSerializer()
    follows_user = serializers.SerializerMethodField()
    id = serializers.UUIDField()


    class Meta:
        model = UserFollowing
        fields = '__all__'

    def get_follows_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            return UserFollowing.objects.filter(following_user=user, followed_user=obj.following_user).exists()
        return False

class UserFollowerSerializer(serializers.ModelSerializer):
    following_user = UserSerializer()

    class Meta:
        model = UserFollowing
        fields = '__all__'

    