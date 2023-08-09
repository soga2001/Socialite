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
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        response = HttpResponse()
        


        try:
            access_token = AccessToken(raw_token)
            pass
        except TokenError as e:
            print('here')
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token is None:
                return None
            try:
                refresh_token = RefreshToken(refresh_token)
            except:
                return None
            
            refresh_token = RefreshToken.for_user(self.get_user(refresh_token.access_token))
            
            raw_token = str(refresh_token.access_token)
            response.set_cookie(
                key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
                value = refresh_token.access_token,
                expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            response.set_cookie(
                key ='refresh_token',
                value = str(refresh_token),
                expires = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            response.close()
            pass


        try:
            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token
        except:
            return None
        
    def authenticate_with_token(self, request, token):
        # try:
        #     validated_token = self.get_validated_token(token)
        #     user = self.get_user(validated_token)
        #     return user, validated_token
        # except TokenError as e:
        #     print('Token error:', e)
        # except Exception as e:
        #     print('Exception:', e)
        # except:
        #     print('here')
        # return None
        try:
            pass
        except:
            pass
    



    

class IsAuthenticated:

    def has_permission(self, request, view):
        # print(view)
        return bool(request.user and request.user.is_authenticated)
    

class IsAdmin:

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
    