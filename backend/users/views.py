# From Django
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

import json
from .serializer import UserSerializer

jwt = JWTAuthentication()

# Create your views here.
def users(request):
    token = get_token(request)
    users = UserSerializer(User.objects.all(), many=True)
    return JsonResponse({'users': list(users.data), 'token': token}, safe=False)

def user_login(request):
    data = json.loads(request.body)
    user = authenticate(username=data['username'], password=data['password'])
    if(user):
        login(request, user)
        token = RefreshToken.for_user(user)
        return JsonResponse({"loggedIn": True, "access_token": str(token.access_token)}, safe=False)
    return JsonResponse({"loggedIn": False}, safe=False)

def user_register(request):
    try:
        data = json.loads(request.body)
        user = User.objects.create_user(
            username=data['username'], 
            password=data['password'], 
            email=data['email'])
        return JsonResponse({"success": True}, safe=False)
    except: 
        return JsonResponse({"error": True, "message":" Username already exists"}, safe=False)


class Delete(APIView):
    permission_classes= [IsAuthenticated]
    def delete(self, request):
        # jwt.authenticate(request) returns user object and a token
        user, token = jwt.authenticate(request)
        return JsonResponse({"success": True}, safe=False)



def delete_all(request):
    User.objects.all().delete()
    return JsonResponse({"success": True}, safe=False)