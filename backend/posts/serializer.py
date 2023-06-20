from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField()
    username = serializers.CharField(source="user.username")
    user_avatar = serializers.FileField(source="user.avatar")
    id = serializers.UUIDField()
    
    class Meta:
        model = Post
        fields = '__all__'

    total_likes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    
    def get_total_likes(self, obj):
        return obj.post_likes.count()
    
    def get_total_comments(self, obj):
        return obj.post_comments.count()