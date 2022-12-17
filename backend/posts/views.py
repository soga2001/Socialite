from time import time
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializer import PostSerializer
from PIL import Image
import uuid
import os

import json

jwt = JWTAuthentication()

class Post_Content(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            image = request.FILES['image']
            caption = request.POST['caption']
            # The following two lines make sure the file uploaded is actually an image
            check_image = Image.open(image)
            check_image.verify()
            user, token = jwt.authenticate(request)
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
    return JsonResponse({"posts": list(posts.data)}, safe=False)

@api_view(["GET"])
def user_posted(request, timestamp, user_id):
    posts = PostSerializer(Post.objects.filter(user_id=user_id).filter(date_posted__lt=timestamp)[:10], many=True)
    return JsonResponse({"posts": list(posts.data)}, safe=False)


@api_view(["GET"])
def view_post_by_id(request, post_id):
    post = PostSerializer(Post.objects.get(pk=post_id))
    print(post.data)
    return JsonResponse({"post": post.data}, safe=False)


@api_view(["DELETE"])
def delete_all_posts(request):
    Post.objects.all().delete()
    return JsonResponse({"success": True}, safe=False)


    
    