from channels.auth import AuthMiddlewareStack
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections

# import django get_user_model()
from django.contrib.auth import get_user_model
# import get_header
from rest_framework_simplejwt.authentication import JWTAuthentication

jwt = JWTAuthentication()

# custom websocket stack
class CustomAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        header = jwt.get_header(scope)
        
        if header is None:
            try:
                raw_token = scope.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
            except:
                scope['user'] = AnonymousUser()
                return self.inner(scope)
        else:
            raw_token = jwt.get_raw_token(header)
        if raw_token is None:
            scope['user'] = AnonymousUser()
            return self.inner(scope)

        try:
            validated_token = jwt.get_validated_token(raw_token)
            user, validated_token = jwt.get_user(validated_token), validated_token
            try:
                user.session_set.get(session_key=scope.session.session_key)
            except Exception as e:
                scope['user'] = AnonymousUser()
                print(scope['user'].is_anonymous)
                return self.inner(scope)
            scope['user'] = user
            return self.inner(scope)
        except:
            scope['user'] = AnonymousUser()
            return self.inner(scope)

CustomAuthMiddlewareStack = lambda inner: CustomAuthMiddleware(AuthMiddlewareStack(inner))
