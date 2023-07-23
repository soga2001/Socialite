from rest_framework import serializers
from .models import Comment

class UUIDField(serializers.Field):
    def to_representation(self, value):
        return str(value)

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    user_avatar = serializers.FileField(source="user.avatar")
    post = serializers.UUIDField()
    
    class Meta:
        model = Comment
        fields = '__all__'



    # total_likes = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    
    # def get_total_likes(self, obj):
    #     return obj.comment_likes.count()

    def get_is_owner(self, instance):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            return user == instance.user
        return False

