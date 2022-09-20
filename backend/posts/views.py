from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializer import PostSerializer
from PIL import Image

import json

jwt = JWTAuthentication()

class Post_Content(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            image = request.FILES['image']
            caption = request.POST['caption']
            print("image file---",image)
            print("caption---", caption)
            # The following two lines make sure the file uploaded is actually an image
            check_image = Image.open(image)
            check_image.verify()
            user, token = jwt.authenticate(request)
            # data = json.loads(request.body)
            # post = Post(
            #     username = user,
            #     user_id = user.id,
            #     img_url = data['img_url'],
            #     caption=data['caption']
            # )
            # post.save()
            # return JsonResponse({"success": True, "post": PostSerializer(post).data}, safe=False)
            return JsonResponse({"error": False}, safe=False)
        except:
            return JsonResponse({"error": True}, safe=False)


@api_view(["GET"])
def view_posts(request):
    posts = PostSerializer(Post.objects.all(), many=True)
    return JsonResponse({"posts": list(posts.data)}, safe=False)


@api_view(["DELETE"])
def delete_posts(request):
    Post.objects.all().delete()
    return JsonResponse({"success": True}, safe=False)