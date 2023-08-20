import re
from time import time
from django.db import DatabaseError
from django.http import JsonResponse
from django.utils.html import escape
from rest_framework.views import APIView
# From Django
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from following.models import UserFollowing
from django.db.models import Q
import time

from notifications.signals import notify


# From rest_framework
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from PIL import Image
from .models import Post
from .serializer import PostSerializer
from users.models import User
from backend.authenticate import *
from rest_framework import status

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

from replace import *

channel_layer = get_channel_layer()
custom = CustomAuthentication()


def user_is_following(following_user, followed_user):
    try:
        UserFollowing.objects.get(following_user=following_user, followed_user=followed_user)
        return True
    except UserFollowing.DoesNotExist:
        return False


class Post_Content(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CustomAuthentication,)

    def post(self, request):
        try:
            image = request.FILES['image']
            caption = request.POST['caption']
            # The following two lines make sure the file uploaded is actually an image
            check_image = Image.open(image)
            check_image.verify()
            caption = escape(caption)
            regex = r'@(\w+)'
            # caption = re.sub(r'@(\w+)', r'<a href="/users/\1/">@\1</a>', caption)
            user_list = []
            caption = re.sub(regex, lambda val: replaceMention(val, user_list), caption)
            caption = replaceLink(caption)
            user = User.objects.get(pk=request.user.id)
            post = Post(
                user = user,
                img_url = image,
                caption=caption
            )
            post.save()
            link = "{}/spill/{}".format(user.username, post.id)

            # followers = list(user.followers.all())

            # notify.send(actor=user, recipient=followers, verb='posted a new spill', target=post, description=link)

            if(user_list): 
                notify.send(actor=user, recipient=user_list, verb='mentioned you', target=post, description=link)

            group_name = f'user_{post.user.username}'
            async_to_sync(channel_layer.group_send)(group_name, {
                "type": "user_update",
                "updateType": 'posted',
                "message": json.dumps(PostSerializer(post, context={'request': request}).data)
            })
            # return JsonResponse({"success": True, "post": PostSerializer(post).data}, safe=False)
            return JsonResponse({"error": False}, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"error": True}, safe=False)

    def delete(self, request):
        data = json.loads(request.body)
        try:
            Post.objects.filter(user_id=request.user.id).filter(id=data["id"]).delete()
            group_name = f'user_{request.user.username}'
            async_to_sync(channel_layer.group_send)(group_name, {
                "type": "user_update",
                "updateType": 'deleted',
                "message": "Post deleted"
            })
            return JsonResponse({"success": True}, safe=False)
        except:
            return JsonResponse({"success": False}, safe=False)

@api_view(["GET"])
def view_posts(request, timestamp, page):
    offset = int(page) * 5
    try:
        post = Post.objects.filter(date_posted__lt=timestamp, user__private=False)[offset:offset+5]
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PostSerializer(post, context={'request': request}, many=True)
    return JsonResponse({"posts": serializer.data}, status=200)


@api_view(["GET"])
@authentication_classes([CustomAuthentication,])
@permission_classes([IsAuthenticated,])
def post_by_followed_users(request, timestamp, page):
    try:
        followed_list = request.user.following.values_list('followed_user_id', flat=True)
        offset = int(page) * 10
        posts = Post.objects.filter(user__in=followed_list).filter(date_posted__lt=timestamp)[offset:offset+10]
        if posts:
            posts = PostSerializer(posts, context={'request': request}, many=True)
            return JsonResponse({"posts": posts.data}, safe=False)
        else:
            if offset == 0:
                return JsonResponse({"message": "You are not following anyone"})
            return JsonResponse({"message": "You have reached the end."})
    except Exception as e:
        return JsonResponse({"error": True, "message": str(e)})

@api_view(["GET"])
def explore(request, timestamp, page):
    offset = int(page) * 10
    try:
        user = request.user
        query = (Q(date_posted__lt=timestamp) & (Q(user__private=False)) | Q(user=user) | Q(user__followers__following_user_id=user.id))
        post = Post.objects.filter(query)[offset:offset+10]
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print("Error in Explore",str(e))
        return JsonResponse({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    

    serializer = PostSerializer(post, context={'request': request}, many=True)
    return JsonResponse({"posts": serializer.data}, status=200)



@api_view(["GET"])
def user_posted(request, timestamp, page, username):
    offset = int(page) * 10
    try:
        user = User.objects.get(username=username)
        if(user.private):
            try:
                user.followers.get(following_user_id=request.user.id).exists()
            except UserFollowing.DoesNotExist as e:
                return JsonResponse({"error": True, "message": "User is private. Please follow them to see their posts."}, status=status.HTTP_404_NOT_FOUND)
        pass
    except User.DoesNotExist:
        return JsonResponse({"error": True, 'message':"User doesn't exist."})
    except Post.DoesNotExist:
        return JsonResponse({"error": True, "message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
    posts = PostSerializer(Post.objects.filter(user__username=username,date_posted__lt=timestamp)[offset:offset+10], context={'request': request}, many=True)
    return JsonResponse({"posts": list(posts.data)}, safe=False)



@api_view(["DELETE"])
def delete_all_posts(request):
    Post.objects.all().delete()
    return JsonResponse({"success": True}, safe=False)


@api_view(["GET"])
def total_user_posted(request, user_id):
    posts = Post.objects.filter(user_id=user_id).count()
    return JsonResponse({"posts": posts}, safe=False)


@api_view(["GET"])
def get_post_by_id(request, post_id):
    try:
        user = request.user
        query = (Q(user__private=False) | Q(user=user) | Q(user__followers__following_user_id=user.id))
        spill = Post.objects.get(pk=post_id)
        if(spill.user.private and spill.user != request.user):
            try:
                query = (Q(user__private=False) | Q(user=user) | Q(following_user_id=user.id))
                spill.user.followers.get(following_user_id=request.user.id)
            except UserFollowing.DoesNotExist as e:
                return JsonResponse({"error": True, "message": "Post not found."}, status=404)
        return JsonResponse({"spill": PostSerializer(spill, context={'request': request}).data}, status=200)
    except Post.DoesNotExist:
        return JsonResponse({"error": True, "message": "Post not found."}, status=404)
    except DatabaseError as e:
        return JsonResponse({"error": True}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"error": True}, safe=False)


    
    