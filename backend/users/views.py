# From Django
from multiprocessing import managers
from django.db import DatabaseError
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# From rest_framework_simplejwt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
# From rest_framework
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

import datetime

import json
from .serializer import UserSerializer

import environ
import os

env = environ.Env()
environ.Env.read_env()

jwt = JWTAuthentication()


def encrypt(value):
    aes = AES.new(env("ENCRYPTION_KEY").encode("utf8"), AES.MODE_CBC)
    return aes.encrypt(value.encode("utf8"), AES.block_size)

def decrypt(value):
    try:
        aes = AES.new(env("ENCRYPTION_KEY").encode("utf8"), AES.MODE_CBC)
        val = aes.decrypt(b64decode(value), AES.block_size)
        print(unpad(val, AES.block_size).decode("utf8"))
        return val
    except Exception as e:
        print('here')
        return value

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

@api_view(["GET"])
def user_by_username(request, username):
    try:
        users = UserSerializer(User.objects.filter(username__contains=username), many=True)
        return JsonResponse({"success": True, "users": users.data}, safe=False)
    except:
        return JsonResponse({"error": True}, safe=False)

@api_view(["POST"])
def user_register(request):
    try:
        data = json.loads(request.body)
        if(data['first_name'] == '' or data['last_name'] == ''):
            raise ValueError('Please enter your name')
        if(data['username'] == ''):
            raise ValueError('Please enter your username')
        if(data['email'] == ''):
            raise ValueError('Please enter your email')
        if(data['password'] == ''):
            raise ValueError('Please enter your password')
        if(data['confirm_password'] == ''):
            raise ValueError('Please enter your confirm password')
        if(data['password'] != data['confirm_password']):
            raise ValueError('Password and confirm password must match')

        user = User.objects.create_user(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'], 
            password=data['password'], 
            email=data['email'])
        return JsonResponse({"success": True}, safe=False)
    except ValueError as e:
        return JsonResponse({"error": True, "message": str(e)}, safe=False)
    except DatabaseError:
        return JsonResponse({"error": True, "message":" Username or email is taken."}, safe=False)

@api_view(["POST"])
def user_login(request):
    data = json.loads(request.body)
    username = decrypt(data['encryptedUsername'])
    print(username)
    # enUser = d(data['username'])
    user = authenticate(username=data['username'], password=data['password'])
    if(user):
        login(request, user)
        token = RefreshToken.for_user(user)
        userSerialized = UserSerializer(user)
        return JsonResponse({"access_token": str(token.access_token), 
                            "at_lifetime": str(token.access_token.lifetime.days) + "d",
                            "refresh_token": str(token),
                            "rt_lifetime": str(token.lifetime.days) + "d",
                            "user": userSerialized.data
                            }, safe=False)
    return JsonResponse({"error": True}, safe=False)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

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


class SuperUser(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        if user.is_superuser:
            return JsonResponse({"message": True}, safe=False)
        return JsonResponse({"message": False}, safe=False)

    def post(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            user.is_superuser = True
            user.save()
            return JsonResponse({"success": True}, safe=False)
        except:
            return JsonResponse({"error": True}, safe=False)

class Staff(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        if user.is_staff:
            return JsonResponse({"message": True}, safe=False)
        return JsonResponse({"message": False}, safe=False)

    def post(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            user.is_staff = True
            user.save()
            return JsonResponse({"success": True}, safe=False)
        except:
            return JsonResponse({"error": True}, safe=False)

# Delete Endpoints
class Delete_User(APIView):
    permission_classes= [IsAuthenticated]

    def delete(self, request):
        try:
            user = User.objects.get(id=request.user.id).delete()
            return JsonResponse({"success": True}, safe=False)
        except:
            return JsonResponse({"error": True}, safe=False)


@api_view(["DELETE"])
@permission_classes([IsAdminUser,])
def delete_all(request):
    User.objects.all().delete()
    return JsonResponse({"success": True}, safe=False)