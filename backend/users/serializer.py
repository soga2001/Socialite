from rest_framework import serializers
# from django.contrib.auth.models import User
from users.models import User
from following.models import UserFollowing

from user_sessions.models import Session
from user_agents import parse
from django.contrib.gis.geoip2 import GeoIP2
g = GeoIP2()

class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}, 
            'email': {'write_only': True},
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
        }
    

    total_posted = serializers.SerializerMethodField()
    total_followers = serializers.SerializerMethodField()
    total_following = serializers.SerializerMethodField()

    is_following = serializers.SerializerMethodField()
    is_current_user = serializers.SerializerMethodField()
    notification_on = serializers.SerializerMethodField()

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
    
    def get_notification_on(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.followers.filter(followed_user=obj, notification=True).exists()
        return False



class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
        }


    total_posted = serializers.SerializerMethodField()
    total_followers = serializers.SerializerMethodField()
    total_following = serializers.SerializerMethodField()


    def get_total_posted(self, obj):
        return obj.user_posted.count()

    def get_total_followers(self, obj):
        return obj.followers.count()

    def get_total_following(self, obj):
        return obj.following.count()


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}, 
            'email': {'write_only':True}, 
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
        }


    total_posted = serializers.SerializerMethodField()
    total_followers = serializers.SerializerMethodField()
    total_following = serializers.SerializerMethodField()
    is_current_user = serializers.SerializerMethodField()

    
    def get_is_current_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            return user == obj
        return False

    def get_total_posted(self, obj):
        return obj.user_posted.count()

    def get_total_followers(self, obj):
        return obj.followers.count()

    def get_total_following(self, obj):
        return obj.following.count()
    

class UserSessionSerializer(serializers.ModelSerializer):

    current_session = serializers.SerializerMethodField()
    device = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    browser = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = '__all__'
        extra_kwargs = {'session_data': {'write_only': True}}

    
    def get_current_session(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.session.session_key == obj.session_key
        return False
    
    
    def get_device(self, obj):
        user_agent = parse(obj.user_agent)
        return user_agent.device.model
        
    def get_browser(self, obj):
        user_agent = parse(obj.user_agent)
        return user_agent.browser.family
        
    def get_location(self, obj):
        try:
            data = g.city(obj.ip)
            return data
        except Exception as e:
            return None
        