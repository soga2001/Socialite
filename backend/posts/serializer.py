from rest_framework import serializers
from .models import Post
from users.serializer import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField()
    user = UserSerializer()
    username = serializers.CharField(source="user.username")
    user_avatar = serializers.FileField(source="user.avatar")
    id = serializers.UUIDField()
    
    class Meta:
        model = Post
        fields = '__all__'

    total_likes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    # is_following = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()
    
    def get_total_likes(self, obj):
        return obj.post_likes.count()
    
    def get_total_comments(self, obj):
        return obj.post_comments.count()
    

    def get_user_has_liked(self, instance):
        request = self.context.get('request')
        print('here')
        if request and request.user.is_authenticated:
            user = request.user
            try:
                print(user.user_liked.all().values())
                # liked = user.post_likes.filter(pk=instance.id).exists()
                return user.user_liked.filter(post_id=instance.id).exists()
            except Exception as e:
                print(e)
        

        return False
    

    # def to_representation(self, instance):
    #     data = super(PostSerializer, self).to_representation(instance)
    #     request = self.context.get('request')
    #     if request and request.user.is_authenticated:
    #         print('here')
    #         user = request.user
    #         print(user, )
    #         data['user'] = UserSerializer(instance.user, context={"request": request}).data
    #     return data

    # def get_is_following(self, instance):
    #     request = self.context.get('request')
    #     if request and request.user.is_authenticated:
    #         user = request.user
    #         return user.following.filter(followed_user=instance.user).exists()
    #     return False