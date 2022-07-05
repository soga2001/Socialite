from django.http import JsonResponse
from django.shortcuts import render
from django.middleware.csrf import get_token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializer import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

import json

# Create your views here.
def users(request):
    token = get_token(request)
    users = UserSerializer(User.objects.all(), many=True)
    return JsonResponse({'users': list(users.data), 'token': token}, safe=False)

def login(request):
    data = json.loads(request.body)
    authenticated = authenticate(username=data['username'], password=data['password'])
    if(authenticated):
        user = User.objects.get(username=data['username'])
        refreshToken = RefreshToken.for_user(user)
        return JsonResponse({"loggedIn": True, "access_token": str(refreshToken.access_token)}, safe=False)
    return JsonResponse({"loggedIn": False}, safe=False)

def register(request):
    try:
        data = json.loads(request.body)
        user = User.objects.create_user(username=data['username'], password=data['password'])
        return JsonResponse({"success": True}, safe=False)
    except: 
        return JsonResponse({"error": True, "message":" Username already exists"}, safe=False)


def delete_all(request):
    User.objects.all().delete()
    return JsonResponse({"success": True}, safe=False)