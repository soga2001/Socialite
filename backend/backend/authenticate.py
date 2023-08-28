# cookieapp/authenticate.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions
from datetime import datetime

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, UntypedToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
# import httpresponse
from django.http import HttpResponse
from functools import wraps
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout


def enforce_csrf(request):
    check = CSRFCheck()
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
    

class CustomAuthentication(JWTAuthentication):
    def authenticate(self, request): 
        header = self.get_header(request)
        
        if header is None:
            try:
                raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
            except:
                return None
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
            user, validated_token = self.get_user(validated_token), validated_token
            try:
                user.session_set.get(session_key=request.session.session_key)
            except Exception as e:
                print(user.is_authenticated)
                return None
            return user, validated_token
        except:
            return None


class CustomTokenAuthentication:

    def authenticate(self,request):
        token = request.COOKIES.get('token')
        if not token:
            return None
        try:
            token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return None
        if not token.user.is_active:
            return None
        return token.user, token

    



    

class IsAuthenticated:
    def has_permission(self, request, view):
        # print(view)
        return bool(request.user and request.user.is_authenticated)
    

class IsStaff:
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_staff or request.user.is_admin))
    

class IsAdmin:
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)
    
class IsAdminOrStaff:
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_admin or request.user.is_staff))
    

class IsSuperuser:
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
    

    