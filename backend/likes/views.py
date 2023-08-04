from django.db import IntegrityError
from django.forms import ValidationError
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
# from django.contrib.auth.models import User
from django.db.models import Prefetch
from .models import PostLikes
from users.models import User
from rest_framework.views import APIView
from .serializer import PostLikesSerializer

from posts.models import Post
from posts.serializer import PostSerializer

import json
from backend.authenticate import *

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
channel_layer = get_channel_layer()



custom = CustomAuthentication()

# Create your views here.

class Like_Post(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CustomAuthentication,)

    def post(self, request):
        data = json.loads(request.body)
        post_id = data['post_id']
        post = Post.objects.get(pk=post_id)
        user, token = custom.authenticate(request)
        try:
            
            like = PostLikes(
                post=post, 
                user=user
            )
            like.save()
            group_name = f'user_{like.user.username}'
            async_to_sync(channel_layer.group_send)(group_name, {
                "type": "user.update",
                "updateType": 'liked',
                "message": json.dumps(PostSerializer(post).data)
            })
            return JsonResponse({"liked": True, "message": "Post liked."}, safe=False)
        except IntegrityError as e:
            PostLikes.objects.get(post=post_id, user=request.user.id).delete()
            group_name = f'spill_{post_id}'
            async_to_sync(channel_layer.group_send)(group_name, {
                "type": "post.update",
                "updateType": 'disliked',
                "message": "Post disliked"
            })
            return JsonResponse({"liked": False, "message": 'Post unliked.'}, safe=False)
        except Exception as e:
            return JsonResponse({"error": True, "message": 'An error occured while trying to like this post. Please try again later.'}, safe=False)


class UserLiked(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CustomAuthentication,)

    def get(self, request, timestamp, page, post_id):
        try:
            liked = PostLikesSerializer(PostLikes.objects.filter(post=post_id, user=request.user.id).exists())
            # return JsonResponse({"success": False, "liked": list(liked)}, safe=False)
            return JsonResponse({"liked": True}, safe=False)
        except:
            return JsonResponse({"error": True, "liked": False}, safe=False)
        

class Check_Liked(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CustomAuthentication,)

    def get(self, request, post_id):
        try:
            liked = PostLikes.objects.filter(post=post_id, user=request.user.id).exists()
            if(liked):
                return JsonResponse({"liked": True}, safe=False)
            return JsonResponse({"liked": False}, safe=False)
        except:
            return JsonResponse({"error": True, "liked": False}, safe=False)

@api_view(["GET"])
def get_liked_post(request, timestamp, page, username):
    offset = int(page) * 10
    try:
        posts = PostLikes.objects.filter(user__username=username, date_liked__lt=timestamp).select_related('post')[offset:offset+10]
        liked_posts = [PostSerializer(p.post).data for p in posts]


        # liked_posts = [PostSerializer(p.post).data for p in posts]
        return JsonResponse({"success": True, "posts": liked_posts}, safe=False)
    except:
        return JsonResponse({"error": True, "message": "An error occured while trying to get user's liked post."}, safe=False)
