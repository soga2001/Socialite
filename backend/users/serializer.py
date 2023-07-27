from rest_framework import serializers
# from django.contrib.auth.models import User
from users.models import User
from following.models import UserFollowing

class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


    total_posted = serializers.SerializerMethodField()
    total_followers = serializers.SerializerMethodField()
    total_following = serializers.SerializerMethodField()

    is_following = serializers.SerializerMethodField()
    is_current_user = serializers.SerializerMethodField()


    def get_total_posted(self, obj):
        return obj.user_posted.count()

    def get_total_followers(self, obj):
        return obj.followers.count()

    def get_total_following(self, obj):
        return obj.following.count()

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            return UserFollowing.objects.filter(following_user=user, followed_user=obj).exists()
        return False
    
    def get_is_current_user(self, instance):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            return user == instance
        return False

    


    # def to_representation(self, instance):
    #     data = super(UserSerializer, self).to_representation(instance)
    #     request = self.context.get('request')
    #     if not request or not request.user.is_authenticated:
    #         data['is_following'] = False
    #     return data