from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    user_avatar = serializers.FileField(source="user.avatar")
    
    class Meta:
        model = Comment
        fields = '__all__'

    # total_likes = serializers.SerializerMethodField()
    
    # def get_total_likes(self, obj):
    #     return obj.comment_likes.count()