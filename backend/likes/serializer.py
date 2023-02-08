from rest_framework import serializers

# from django.contrib.auth.models import User
from .models import PostLikes

class PostLikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostLikes
        fields = '__all__'

    