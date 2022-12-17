import json
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework.views import APIView
from PIL import Image

from .serializer import UserProfileSerializer

jwt = JWTAuthentication()


class Update_Profile(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            avatar = request.FILES['avatar']
            print('potato')
            bio = request.POST['bio']
            # The following two lines make sure the file uploaded is actually an image
            check_image = Image.open(avatar)
            check_image.verify()
            user = User.objects.get(pk=request.user.id)
            user.profile.bio = bio
            user.profile.avatar = avatar
            user.save()
            return JsonResponse({"error": False}, safe=False)
        except:
            return JsonResponse({"error": True}, safe=False)


@api_view(["GET"])
def get_profile(request, user_id):
    user_id = User.objects.get(pk=user_id)
    profile = UserProfileSerializer(user_id.profile)

    return JsonResponse({"success": True, "user_profile": profile.data}, safe=False)
