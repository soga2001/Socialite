from django.shortcuts import render
from rest_framework import APIView
from django.db import DatabaseError, IntegrityError
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import authentication_classes

from authenticate import CustomAuthentication, IsAuthenticated
from models import PostViews


custom = CustomAuthentication()
# Create your views here.

class PostView(APIView):
    permisson_class = [IsAuthenticated],
    authentication_classes = (CustomAuthentication,)

    def post(self, request, post_id):
        try:
            post = PostViews(
                post_id=post_id,
                user_id=request.user.id
            )
            post.save()
            return JsonResponse({"success": True, "message": "Post viewed"}, safe=False)
        except IntegrityError as e:
            return JsonResponse({"success": True, "message": 'Post already viewed.'}, safe=False)
        except Exception as e:
            return JsonResponse({"error": True, "message": 'An error occured while trying to view this post. Please try again later.'}, safe=False)
