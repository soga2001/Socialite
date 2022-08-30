from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField()
    # username = serializers.CharField()
    username = serializers.CharField()
    class Meta:
        model = Post
        fields = '__all__'