from django.http import HttpResponse
from functools import wraps
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.conf import settings

def refresh_cookies(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        response = view_func(self, request, *args, **kwargs)
        
        try:
            access_token_cookie = self.request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
            refresh_token_cookie = self.request.COOKIES.get('refresh_token')
        except:
            access_token_cookie = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
            refresh_token_cookie = request.COOKIES.get('refresh_token')
            
        if access_token_cookie is None or refresh_token_cookie is None:
            return response
        
        try:
            AccessToken(access_token_cookie)
        except:
            try:
                refresh_token = RefreshToken(refresh_token_cookie)
            except:
                return response
            
            refresh_token = RefreshToken.for_user(refresh_token.access_token.get('user'))
            new_access_token = str(refresh_token.access_token)
            
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=new_access_token,
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
        
        return response
    return _wrapped_view
