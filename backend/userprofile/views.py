import json
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework.views import APIView

from .serializer import UserProfileSerializer




jwt = JWTAuthentication()

# Create your views here.
# def update_profile(request, user_id):
#     user = User.objects.get(pk=user_id)
#     user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
#     user.save()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    data = json.loads(request.body)
    bio = data['bio']
    avatar = data['avatar']
    u = User.objects.get(pk=request.user.id)
    u.profile.bio = bio
    u.profile.avatar = avatar
    u.save()
    return JsonResponse({"success": True}, safe=False)

@api_view(["GET"])
def get_profile(request, user_id):
    user_id = User.objects.get(pk=user_id)
    profile = UserProfileSerializer(user_id.profile)

    return JsonResponse({"success": True, "user_profile": profile.data}, safe=False)
