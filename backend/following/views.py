from django.db import IntegrityError
from django.forms import ValidationError
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from users.serializer import UserSerializer

# from django.contrib.auth.models import User
from users.models import User 
from .models import UserFollowing
from rest_framework.views import APIView
from .serializer import *
from backend.authenticate import *
# from notifications.signals import notify

custom = CustomAuthentication()

# Create your views here.


class Follow_User(APIView):
    authentication_classes = (CustomAuthentication,)
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            if(int(request.user.id) == int(user_id)):
                return JsonResponse({"error": True, "message": 'You cannot follow yourself.'}, safe=False)
        except:
            return JsonResponse({"error": True, "message": 'Invalid User Id'}, safe=False)

        followed_user = User.objects.get(pk=user_id)

        try:
            
            follow = UserFollowing(
                followed_user=followed_user, 
                following_user=request.user
            )
            follow.save()

            link=f'{request.user.username}'
            
            return JsonResponse({"success": True, "message": "User followed"}, safe=False)
        except IntegrityError as e:
            unfollow = UserFollowing.objects.filter(followed_user=user_id, following_user=request.user.id).delete()
            return JsonResponse({"success": True, "message": 'User unfollowed.'}, safe=False)
        except Exception as e:
            return JsonResponse({"error": True, "message": 'An error occured while trying to follow this user. Please try again later.'}, safe=False)
        
    def put(self, request, user_id):
        try:
            follow = UserFollowing.objects.get(followed_user=user_id, following_user=request.user.id)
            follow.notification = not follow.notification
            follow.save()
            return JsonResponse({"success": True, "message": 'Notification status changed.', 'notification_on': follow.notification}, safe=False)
        except UserFollowing.DoesNotExist as e:
            return JsonResponse({"error": True, "message": 'You are not following this user.'}, safe=False)
        except:
            return JsonResponse({"error": True, "message": 'An error occured while trying to change notification status. Please try again later.'}, safe=False)


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
    


# get followers
class GetFollowers(APIView):

    def get(self, request, username):
        user = User.objects.get(username=username)
        try:
            followers = UserFollowerSerializer(UserFollowing.objects.filter(followed_user=user), context={"request": request}, many=True).data
            return JsonResponse({"success": True})
        except Exception as e:
            print(e)
            return JsonResponse({"error": True})
    

# get following
class GetFollowing(APIView):
        def get(self, request, username):

            try:
                user = User.objects.get(username=username)

                following = UserFollowingSerializer(UserFollowing.objects.filter(following_user=user), context={"request": request}, many=True).data

                return JsonResponse({"success": True, "users": following})
            except Exception as e:
                print(e)
                return JsonResponse({"error": True})