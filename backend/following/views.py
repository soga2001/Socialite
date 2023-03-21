from django.db import IntegrityError
from django.forms import ValidationError
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
# from django.contrib.auth.models import User
from users.models import User 
from .models import UserFollowing
from rest_framework.views import APIView
from .serializer import UserFollowingSerializer


jwt = JWTAuthentication()

# Create your views here.


class Follow_User(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            if(int(request.user.id) == int(user_id)):
                return JsonResponse({"error": True, "message": 'You cannot follow yourself.'}, safe=False)
        except:
            return JsonResponse({"error": True, "message": 'Invalid User Id'}, safe=False)

        followed_user = User.objects.get(pk=user_id)
        following_user, token = jwt.authenticate(request)
        # following_user = User.objects.get(pk=request.user.id)

        try:
            # user = User.objects.get(pk=request.user.id)
            # user.following.add(user_id)
            # user.save()
            
            follow = UserFollowing(
                followed_user=followed_user, 
                following_user=following_user
            )
            follow.save()
            return JsonResponse({"success": True, "message": "User followed"}, safe=False)
        except IntegrityError as e:
            unfollow = UserFollowing.objects.filter(followed_user=user_id, following_user=request.user.id).delete()
            return JsonResponse({"success": True, "message": 'User unfollowed.'}, safe=False)
        except Exception as e:
            return JsonResponse({"error": True, "message": 'An error occured while trying to follow this user. Please try again later.'}, safe=False)


@api_view(["GET"])
def get_followers(request, timestamp, page, user_id):
    try:
        followers = UserFollowingSerializer(UserFollowing.objects.filter(followed_user=user_id), many=True).data
        return JsonResponse({"error": False, "followers": list(followers)}, safe=False)
    except:
        return JsonResponse({"error": True, "message": 'An error occured while trying to get followers. Please try again later.'}, safe=False)

@api_view(["GET"])
def get_following(request, timestamp, page, user_id):
    try:
        following = UserFollowingSerializer(UserFollowing.objects.filter(following_user=user_id), many=True).data
        return JsonResponse({"error": False, "following": list(following)}, safe=False)
    except:
        return JsonResponse({"error": True, "message": 'An error occured while trying to get following. Please try again later.'}, safe=False)


@api_view(["GET"])
def get_followed_by_id(request, user_id):
    try:
        followed = UserFollowing.objects.filter(followed_user=user_id, following_user=request.user.id).exists()
        return JsonResponse({"success": False, "followed": followed}, safe=False)
    except:
        return JsonResponse({"error": True, "followed": False}, safe=False)