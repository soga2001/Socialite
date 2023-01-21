from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField()
    username = serializers.CharField(source="user.username")
    user_avatar = serializers.FileField(source="user.profile.avatar")
    class Meta:
        model = Post
        fields = '__all__'