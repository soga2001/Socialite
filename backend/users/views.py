from django.forms import ImageField
from django.shortcuts import get_object_or_404
from backend.authenticate import *
# From Django
from django.conf import settings
from django.core import serializers
from django.db import DatabaseError, IntegrityError
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt, csrf_protect, requires_csrf_token
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import F

# from django.contrib.postgres.search import TrigramSimilarity, TrigramDistance, TrigramWordSimilarity
from django.db.models import Q


from django.contrib.sessions.models import Session
from backend.encryption import *


# From rest_framework_simplejwt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
# From rest_framework
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import authentication_classes
# from rest_framework.authtoken.models import Token
from tokens.models import Tokens



from users.models import User
from .serializer import *
from backend.decorators import refresh_cookies
from backend.encryption import AESCipher

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


import datetime
from django.utils import timezone

import json
from PIL import Image

import environ

env = environ.Env()
environ.Env.read_env()

jwt = JWTAuthentication()
custom = CustomAuthentication()

# Create your views here.
@api_view(["GET"])
def get_csrf(request):
    csrf = get_token(request)
    return JsonResponse({'csrf': csrf})

@api_view(["GET"])
def flush_session(request):
    request.session.flush()
    return JsonResponse({'success': True})

@api_view(["GET"])
def users(request):
    users = UserSerializer(User.objects.all(), context={'request': request}, many=True)
    return JsonResponse({'users': list(users.data)}, safe=False)

@api_view(["GET"])
def user_by_id(request, user_id):
    try:
        user = UserSerializer(User.objects.filter(id=user_id), many=True)
        return JsonResponse({"success": True, "user": user.data}, safe=False)
    except:
        return JsonResponse({"error": True}, safe=False)


@api_view(["GET"])
def user_by_username(request, username, multiple = True):
    try:
        if(multiple == True):
            users_data = User.objects.filter(username__icontains=username, is_active=True)
            users_data = UserSerializer(users_data,context={'request': request}, many=True).data
        else:
            # users_data = User.objects.get(username=username)
            # users_data = UserSerializer(users_data, context={'request', request}).data
            users_data = User.objects.get(username=username)
            users_data = UserSerializer(users_data, context={'request': request}).data
        if(len(users_data) == 0):
            return JsonResponse({"error": "User does not exist"}, status=404)
        return JsonResponse({"success": True, "users": users_data})
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({"error": "An error occurred"}, status=500)




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
        return JsonResponse({"success": True, 'message': 'An email has been sent to your email. Please click on the link to verify your email.'}, safe=False)
    except ValueError as e:
        return JsonResponse({"error": True, "message": str(e)}, safe=False)
    except DatabaseError:
        return JsonResponse({"error": True, "message":" Username or email is taken."}, safe=False)

@api_view(["POST"])
def user_login(request):
    data = json.loads(request.body)
    user = authenticate(username=data['username'], password=data['password'])
    print(user is not None)
    if(user and user.email_verified):
        login(request, user)
        token = RefreshToken.for_user(user)
        request.session.set_test_cookie()


        response = JsonResponse({"success": True, "user": UserSerializer(user).data}, status=200)
        # response.set_cookie("testing", "true", secure=True, httponly=True)
        response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
                    value = str(token.access_token),
                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        # response.set_cookie('access_token', str(token.access_token), expires=str(token.access_token.lifetime.days) + "d", secure=True, httponly=True)
        response.set_cookie('refresh_token', str(token), expires=str(token.lifetime.days)+ "d", secure=True, httponly=True)
        return response
    elif user and not user.email_verified:
        return JsonResponse({"error": True, "message": "Please verify your email."}, safe=False)
    else:
        return JsonResponse({"error": True, "message": "Invalid credentials."}, safe=False)
    # return JsonResponse({"error": True}, safe=False)

@api_view(["POST"])
def verify_email(request):
    try:
        token = json.loads(request.body)['token']
        # decrypted_msg = AESCipher().decrypt(token.replace(' ', '+'))
        token = Tokens.objects.get(key=token)
        if token.expires_at < timezone.now():
            token.delete()
            return JsonResponse({"error": True, "message": "the Token has expired"})
        user = token.user
        user.email_verified = True
        user.save()
        token.delete()
        return JsonResponse({"success": True, "message": "Email has been verified."})
    except Tokens.DoesNotExist as e:
        return JsonResponse({"error": True, "message": "token is invalid"})
    except Exception as e:
        return JsonResponse({'"error': True, "message": "token is invalid"})
    
@api_view(["POST"])
def email_forgot_password_link(request):
    data = json.loads(request.body)
    user = User.objects.get(email=data['email'])
    try:
        expires_at = datetime.datetime.now() + datetime.timedelta(minutes=10)
        token = Tokens.objects.create(user=user, expires_at=expires_at)
    except User.DoesNotExist:
        return JsonResponse({"error": True, "message": "User does not exist."})
    except IntegrityError as e:
        token = Tokens.objects.get(user=user)
        token.delete()
        token = Token.objects.create(user=user)
    except Exception as e:
        print('exception',e)
        return JsonResponse({"error": True, "message": "An error occurred."}, safe=False)
    subject = 'Reset your password'
    html_message = render_to_string('emails/reset_password.html', {'reset_link': settings.RESET_PASSWORD_URL + token.key, 'first_name': user.first_name})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    return JsonResponse({"success": True})
    
@api_view(["PUT"])
def reset_password(request):
    try:
        data = json.loads(request.body)
        token = Tokens.objects.get(key=data['token'])
        
        user = token.user
        if(data['password'] == data['confirm_password']):
            user.set_password(data['password'])
            user.save()
            token.delete()
        else:
            return JsonResponse({'error': True, 'message': "Password and Confirm Password has to match."})
        return JsonResponse({"success": True})
    except IntegrityError as e:

        return JsonResponse({"error": True, "message": "Invalid token."}, safe=False)
    except Exception as e:
        return JsonResponse({'"error': True})

@api_view(["GET"])
def get_session(request):
    if "access_token" in request.COOKIES:
        request.COOKIES.get('access_token')
    return JsonResponse({"success": True})

    
class UserFromCookie(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomAuthentication,]

    # @refresh_cookies
    def get(self, request):
        user, token = custom.authenticate(request)
        try:
            # print(AESCipher().decrypt(encrypted))
            user = UserSerializer(request.user).data
            return JsonResponse({"success": True, "user": user})
        except:
            return JsonResponse({"success": False, "message": "User not found."})


class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomAuthentication,]

    def post(self, request):
        try:
            # if 'avatar' in json.loads(request.body):
            #     print('lol')
            avatar = None
            banner = None
            bio = None
            first_name = None
            last_name = None

            if 'avatar' in request.FILES:
                avatar = request.FILES['avatar']
                try:
                    check_image = Image.open(avatar)
                    check_image.verify()
                except Exception as e:
                    return JsonResponse({"error": True, "message": "Invalid image file."})

            if 'banner' in request.FILES:
                banner = request.FILES['banner']
                try:
                    check_image = Image.open(banner)
                    check_image.verify()
                except Exception as e:
                    return JsonResponse({"error": True, "message": "Invalid image file."})
                
            if 'bio' in request.POST:
                bio = request.POST['bio']
            if 'first_name' in request.POST:
                first_name = request.POST['first_name']
            if 'last_name' in request.POST:
                last_name = request.POST['last_name']

            user = request.user
            if(first_name):
                user.first_name = first_name
            if(last_name):
                user.last_name = last_name
            if(bio):
                user.bio = bio
            if(avatar):
                user.avatar = avatar
            if(banner):
                user.banner = banner
            user.save()
            
            updatedUser = UserSerializer(user).data
            return JsonResponse({"success": True, "user": updatedUser,  "message": "Profile Updated."})
        except Exception as e:
            print(e)
            return JsonResponse({"error": True, "message": str(e)}, status=500)
        except:
            return JsonResponse({"error": True}, status=404)
        

class ChangePassword(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [CustomAuthentication,]

    def put(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            current_password = data['current_password']
            new_password = data['new_password']
            confirm_password = data['confirm_password']
            if(not user.check_password(current_password)):
                return JsonResponse({"error": True, "message": "Current password is incorrect."})
            if(new_password != confirm_password):
                return JsonResponse({"error": True, "message": "Password and confirm password must match."})
            
            user.set_password(new_password)
            user.save()
            return JsonResponse({"success": True, "message": "Your password has been changed."})
        except Exception as e:
            return JsonResponse({"error": True, "message": "An error occurred."}, status=500)
        except:
            return JsonResponse({"error": True}, status=404)
        
class UserInfo(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [CustomAuthentication,]

    def get(self, request):
        try:
            password = request.query_params['password']
            user = User.objects.get(id=request.user.id)
            if(not user.check_password(password)):
                return JsonResponse({"error": True, "message": "Password is incorrect."})
            user = UserInfoSerializer(user).data
            return JsonResponse({"success": True, "user": user})
        except Exception as e:
            return JsonResponse({"error": True}, status=500)
        except:
            return JsonResponse({"error": True}, status=404)
        
class DeleteAccount(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [CustomAuthentication,]

    def delete(self, request):
        try:
            password = request.query_params['password']
            user = User.objects.get(pk=request.user.id)
            if(not user.check_password(password)):
                return JsonResponse({"error": True, "message": "Invalid Password"}, status=401)
            user.delete()
            logout(request)
            response = JsonResponse({"success": True, "message": "Account deleted."}, status=200)
            for cookies in request.COOKIES:
                if cookies != "theme":
                    print(cookies)
                    response.delete_cookie(cookies)
            request.session.flush()
            return response
        except Exception as e:
            print(e)
            return JsonResponse({"error": True}, status=500)
        except:
            return JsonResponse({"error": True}, status=404)
        

class LogoutView(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = (CustomAuthentication,)

    def post(self, request):
        try:
            
            logout(request)
            response = JsonResponse({"success": True}, status=200)
            for cookies in request.COOKIES:
                if cookies != "theme":
                    response.delete_cookie(cookies)
            request.session.flush()
            return response
        except:
            return JsonResponse({"error": True})


class AllLogins(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [CustomAuthentication,]

    def get(self, request):
        user = request.user
        userSerialized = UserSerializer(user)
        return JsonResponse({'success': True, 'user': userSerialized.data, 'sessions': list(Session.objects.all().values())})
        

class LogoutFromAll(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [CustomAuthentication,]

    def delete(self, request):
        sessions = Session.objects.filter(expire_date__gte=datetime.timezone.now(), 
                                       session_key__contains=request.user_id)

        # Delete the sessions
        sessions.delete()


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






@api_view(["DELETE"])
# @permission_classes([IsAdminUser,])
def delete_all(request):
    User.objects.all().delete()
    return JsonResponse({"success": True}, safe=False)