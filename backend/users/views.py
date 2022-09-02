# From Django
import re
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# From rest_framework_simplejwt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
# From rest_framework
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes

import datetime

import json
from .serializer import UserSerializer

jwt = JWTAuthentication()

# Create your views here.
@api_view(["GET"])
def get_csrf(request):
    csrf = get_token(request)
    return JsonResponse({'csrf': csrf})

@api_view(["GET"])
def users(request):
    users = UserSerializer(User.objects.all(), many=True)
    return JsonResponse({'users': list(users.data)}, safe=False)

@api_view(["GET"])
def user_by_id(request, user_id):
    try:
        user = UserSerializer(User.objects.filter(id=user_id), many=True)
        return JsonResponse({"success": True, "user": user.data}, safe=False)
    except:
        return JsonResponse({"error": True}, safe=False)
    


@api_view(["POST"])
def user_register(request):
    try:
        data = json.loads(request.body)
        user = User.objects.create_user(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'], 
            password=data['password'], 
            email=data['email'])
        return JsonResponse({"success": True}, safe=False)
    except: 
        return JsonResponse({"error": True, "message":" Username or email is taken."}, safe=False)

@api_view(["POST"])
def user_login(request):
    data = json.loads(request.body)
    user = authenticate(username=data['username'], password=data['password'])
    if(user):
        login(request, user)
        token = RefreshToken.for_user(user)
        return JsonResponse({"access_token": str(token.access_token), 
                            "at_lifetime": str(token.access_token.lifetime.days) + "d",
                            "refresh_token": str(token),
                            "rt_lifetime": str(token.lifetime.days) + "d"
                            }, safe=False)
    return JsonResponse({"loggedIn": False}, safe=False)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user, token = jwt.authenticate(request)
            data = json.loads(request.body)
            rt_token = RefreshToken(data['refresh_token'])
            rt_token.blacklist()
            logout(request)
            return JsonResponse({"success": True}, safe=False)
        except:
            return JsonResponse({"error": True}, safe=False)

# Delete Endpoints
class Delete(APIView):
    permission_classes= [IsAuthenticated]
    def delete(self, request):
        # jwt.authenticate(request) returns user object and a token
        user, token = jwt.authenticate(request)
        return JsonResponse({"success": True}, safe=False)

@api_view(["DELETE"])
# @permission_classes([IsAuthenticated])
def delete_all(request):
    User.objects.all().delete()
    return JsonResponse({"success": True}, safe=False)