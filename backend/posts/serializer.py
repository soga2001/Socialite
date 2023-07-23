from rest_framework import serializers
from .models import Post
from users.serializer import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField()
    user = UserSerializer()
    id = serializers.UUIDField()
    
    class Meta:
        model = Post
        fields = '__all__'

    total_likes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    
    def get_total_likes(self, obj):
        return obj.post_likes.count()
    
    def get_total_comments(self, obj):
        return obj.post_comments.count()
    

    def get_user_has_liked(self, instance):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            try:
                return user.user_liked.filter(post_id=instance.id).exists()
            except Exception as e:
                return False

        return False
    
    def get_is_owner(self, instance):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            return user == instance.user
        return False