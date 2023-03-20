from rest_framework import serializers
# from django.contrib.auth.models import User
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    # user_posted = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    total_posted = serializers.SerializerMethodField()
    total_followers = serializers.SerializerMethodField()
    total_following = serializers.SerializerMethodField()


    def get_total_posted(self, obj):
        return obj.user_posted.count()

    def get_total_followers(self, obj):
        return obj.following.count()

    def get_total_following(self, obj):
        return obj.followers.count()
        # return obj.following.filter(following_user=self).count()