from django.db import IntegrityError
from django.forms import ValidationError
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from posts.models import Post
from .models import PostLikes
from rest_framework.views import APIView
from .serializer import PostLikesSerializer


jwt = JWTAuthentication()

# Create your views here.

class Like_Post(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):

        post = Post.objects.get(post=post_id)
        user, token = jwt.authenticate(request)
        # following_user = User.objects.get(pk=request.user.id)

        try:
            # user = User.objects.get(pk=request.user.id)
            # user.following.add(user_id)
            # user.save()
            
            like = PostLikes(
                post=post, 
                user=user
            )
            like.save()
            return JsonResponse({"liked": True, "message": "Post liked."}, safe=False)
        except IntegrityError as e:
            PostLikes.objects.filter(post=post_id, user=request.user.id).delete()
            return JsonResponse({"liked": False, "message": 'Post unliked.'}, safe=False)
        except Exception as e:
            return JsonResponse({"error": True, "message": 'An error occured while trying to like this post. Please try again later.'}, safe=False)


class UserLiked(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, timestamp, page, post_id):
        try:
            liked = PostLikesSerializer(PostLikes.objects.filter(post=post_id, user=request.user.id).exists()).data
            return JsonResponse({"success": False, "liked": list(liked)}, safe=False)
        except:
            return JsonResponse({"error": True, "liked": False}, safe=False)

@api_view(["GET"])
def get_liked(request, timestamp, page, user_id):
    try:
        liked = PostLikesSerializer(PostLikes.objects.filter(user=user_id), many=True).data
        return JsonResponse({"error": False, "followers": list(liked)}, safe=False)
    except:
        return JsonResponse({"error": True, "message": 'An error occured while trying to get followers. Please try again later.'}, safe=False)

# @api_view(["GET"])
# def get_following(request, timestamp, page, user_id):
#     try:
#         following = PostLikesSerializer(PostLikes.objects.filter(following_user=user_id), many=True).data
#         return JsonResponse({"error": False, "following": list(following)}, safe=False)
#     except:
#         return JsonResponse({"error": True, "message": 'An error occured while trying to get following. Please try again later.'}, safe=False)


# @api_view(["GET"])
# def get_liked_by_id(request, post_id):
#     try:
#         followed = PostLikes.objects.filter(post=post_id, following_user=request.user.id).exists()
#         return JsonResponse({"success": False, "followed": followed}, safe=False)
#     except:
#         return JsonResponse({"error": True, "followed": False}, safe=False)