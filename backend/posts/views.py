import re
from time import time
from django.http import JsonResponse
from django.utils.html import escape
from rest_framework.decorators import api_view
from rest_framework.views import APIView
# From Django
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect, requires_csrf_token
# from django.contrib.auth.models import User

# From rest_framework
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from PIL import Image
from .models import Post
from .serializer import PostSerializer
from users.models import User
from backend.authenticate import *


import json

custom = CustomAuthentication()

def replace(val):
    u = re.sub(r'@', '', val.group())
    try:
        user = User.objects.get(username=u)
        if user:
            return r'<a href="/profile/user/{0}/">@{0}</a>'.format(u)
        else:
            return val
    except User.DoesNotExist:
        return r'{0}'.format(val.group())


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
            caption = re.sub(regex, replace, caption)
            user, token = custom.authenticate(request)
            post = Post(
                user = user,
                img_url = image,
                caption=caption
            )
            post.save()
            # return JsonResponse({"success": True, "post": PostSerializer(post).data}, safe=False)
            return JsonResponse({"error": False}, safe=False)
        except:
            return JsonResponse({"error": True}, safe=False)

    def delete(self, request):
        data = json.loads(request.body)
        try:
            Post.objects.filter(user_id=request.user.id).filter(id=data["id"]).delete()
            return JsonResponse({"success": True}, safe=False)
        except:
            return JsonResponse({"success": False}, safe=False)

@api_view(["GET"])
def view_posts(request, timestamp, page):
    offset = int(page) * 5
    posts = PostSerializer(Post.objects.filter(date_posted__lt=timestamp)[offset:offset+5], many=True)
    return JsonResponse({"posts": posts.data}, safe=False)


@api_view(["GET"])
@authentication_classes([CustomAuthentication,])
@permission_classes([IsAuthenticated,])
def post_by_followed_users(request, timestamp, page):
    try:
        followed_list = request.user.following.values_list('followed_user_id', flat=True)
        offset = int(page) * 10
        posts = PostSerializer(Post.objects.filter(user__in=followed_list).filter(date_posted__lt=timestamp)[offset:offset+10], many=True)
        if posts:
            return JsonResponse({"posts": posts.data}, safe=False)
        else:
            if offset == 0:
                return JsonResponse({"message": "You are not following anyone"})
            return JsonResponse({"message": "You have reached the end."})
    except Exception as e:
        return JsonResponse({"error": True, "message": str(e)})

@api_view(["GET"])
def explore(request, offset):
    if 'displayed_post_ids' not in request.session:
        request.session['displayed_post_ids'] = []
    displayed_post_ids = request.session['displayed_post_ids']
    if int(offset) < len(displayed_post_ids):
        newList = displayed_post_ids[int(offset):int(offset) + 10]
        posts = Post.objects.filter(pk__in=newList)
    else:
        post_ids = Post.objects.exclude(id__in=displayed_post_ids).order_by('?').values_list('id', flat=True)[:10]
        posts = Post.objects.filter(pk__in=post_ids).order_by('?')
        displayed_post_ids += list(post_ids)
        request.session['displayed_post_ids'] = displayed_post_ids

    

    if len(posts) == 0:
        return JsonResponse({"message": "You have viewed all the unique posts."})

    posts = PostSerializer(posts, many=True)
    return JsonResponse({"posts": posts.data})



@api_view(["GET"])
def user_posted(request, timestamp, page, username):
    posts = PostSerializer(Post.objects.filter(user__username=username).filter(date_posted__lt=timestamp)[:10], many=True)
    return JsonResponse({"posts": list(posts.data)}, safe=False)


@api_view(["GET"])
def view_post_by_id(request, post_id):
    try:
        post = PostSerializer(Post.objects.get(pk=post_id))
        return JsonResponse({"post": post.data})
    except:
        return JsonResponse({"error": True, "message": "Post not found."})


@api_view(["DELETE"])
def delete_all_posts(request):
    Post.objects.all().delete()
    return JsonResponse({"success": True}, safe=False)


@api_view(["GET"])
def total_user_posted(request, user_id):
    posts = Post.objects.filter(user_id=user_id).count()
    return JsonResponse({"posts": posts}, safe=False)



    
    