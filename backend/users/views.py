from django.forms import ImageField, ValidationError
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
# import JWTAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.dateparse import parse_date

# from django.contrib.postgres.search import TrigramSimilarity, TrigramDistance, TrigramWordSimilarity
from django.db.models import Q
# import escape
from django.utils.html import escape
from dateutil.parser import parse


# from django.contrib.sessions.models import Session
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

# @api_view(["GET"])
# @authentication_classes([CustomAuthentication])
# @permission_classes([IsAdmin,])
class AllUsers(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    authentication_classes = [CustomAuthentication,]

    def get(self, request):
        try:
            users = User.objects.all()
            users = UserSerializer(users, context={'request': request}, many=True).data
            return JsonResponse({"success": True, "users": users})
        except Exception as e:
            return JsonResponse({"error": True, "message": "An error occurred."})
# def users(request):
#     users = UserSerializer(User.objects.all(), context={'request': request}, many=True)
#     return JsonResponse({'users': list(users.data)}, safe=False)

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
            return JsonResponse({"error": "User does not exist"})
        return JsonResponse({"success": True, "users": users_data})
    except User.DoesNotExist:
        return JsonResponse({"error": True, "message": "User does not exist"})
    except Exception as e:
        return JsonResponse({"error": True, "message": "An error occurred"})




@api_view(["POST"])
def user_register(request):
    try:
        data = json.loads(request.body)
        print(data)

        user = User.objects.create_user(
            full_name=data['full_name'],
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

    def get(self, request):
        try:
            user = custom.authenticate(request)
        except Exception as e:
            response = JsonResponse({'error': True})
            return response
        try:
            user = UserSerializer(request.user).data
            return JsonResponse({"success": True, "user": user})
        except Exception as e:
            response = JsonResponse({'error': True})
            refresh_token = request.COOKIES.get('refresh_token')
            if(refresh_token):
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                except:
                    pass

                for cookies in request.COOKIES:
                    if cookies != "theme":
                        response.delete_cookie(cookies)
                request.session.flush()
            return response


class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomAuthentication,]

    def post(self, request):
        try:
            avatar = None
            banner = None
            bio = None
            full_name = None
            link = None
            location = None

            user = request.user


            if 'avatar' in request.FILES:
                avatar = request.FILES['avatar']
                try:
                    check_image = Image.open(avatar)
                    check_image.verify()
                    user.avatar = avatar
                except Exception as e:
                    print(e)
                    return JsonResponse({"error": True, "message": "Invalid image file."})

            if 'banner' in request.FILES:
                banner = request.FILES['banner']
                try:
                    check_image = Image.open(banner)
                    check_image.verify()
                    user.banner = banner
                except Exception as e:
                    print(e)
                    return JsonResponse({"error": True, "message": "Invalid image file."})
                
            
            if 'bio' in request.POST:
                bio = request.POST['bio']
                user.bio = escape(bio)
            if 'full_name' in request.POST:
                full_name = request.POST['full_name']
                user.full_name = escape(full_name)
            if 'link' in request.POST:
                link = request.POST['link']
                user.link = escape(link)
            if 'location' in request.POST:
                location = request.POST['location']
                user.location = escape(location)
            if 'dob' in request.POST:
                dob = request.POST['dob']
                user.dob = str(dob)
            user.save()
            updatedUser = UserSerializer(user).data
            return JsonResponse({"success": True, "user": updatedUser,  "message": "Profile Updated."})
        except ValidationError as e:
            print(e)
            return JsonResponse({"error": True, "message": str(e.message)})
        except Exception as e:
            print(e)
            return JsonResponse({"error": True, "message": str(e)})
        except:
            return JsonResponse({"error": True})
        

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
            user.session_set.filter(~Q(session_key=request.session.session_key)).delete()
            return JsonResponse({"success": True, "message": "Your password has been changed."})
        except Exception as e:
            return JsonResponse({"error": True, "message": "An error occurred."}, status=500)
        except:
            return JsonResponse({"error": True}, status=404)
        

class DeleteCookies(APIView):
    def delete(self, request):
        try:
            response = JsonResponse({"success": True}, status=200)
            for cookies in request.COOKIES:
                if cookies != "theme":
                    response.delete_cookie(cookies)
            request.session.flush()
            return response
        except:
            return JsonResponse({"error": True})
        
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
                    response.delete_cookie(cookies)
            request.session.flush()
            return response
        except Exception as e:
            print(e)
            return JsonResponse({"error": True}, status=500)
        except:
            return JsonResponse({"error": True}, status=404)
        
class Staff(APIView):
    permission_classes = [IsAdmin, IsAuthenticated]
    authentication_classes = [CustomAuthentication,]

    def post(self, request):
        try:
            user_id = request.query_params['user_id']
            user = User.objects.get(pk=user_id)
            user.is_staff = True
            user.save()
            return JsonResponse({"success": True, "message": "User is now a staff."})
        except Exception as e:
            return JsonResponse({"error": True}, status=500)
        except:
            return JsonResponse({"error": True}, status=404)
        
    def delete(self, request):
        try:
            user_id = request.query_params['user_id']
            user = User.objects.get(pk=user_id)
            user.is_staff = False
            user.save()
            return JsonResponse({"success": True, "message": "User is no longer a staff."})
        except Exception as e:
            return JsonResponse({"error": True}, status=500)
        except:
            return JsonResponse({"error": True}, status=404)
        
        
class VerifyUser(APIView):
    permission_classes = [IsAdminOrStaff, IsAuthenticated]
    authentication_classes = [CustomAuthentication,]

    def post(self, request):
        try:
            user_id = request.query_params['user_id']
            user = User.objects.get(pk=user_id)
            user.verified = True
            user.save()
            return JsonResponse({"success": True, "message": "User is now verified."})
        except Exception as e:
            return JsonResponse({"error": True}, status=500)
        except:
            return JsonResponse({"error": True}, status=404)
        
    def delete(self, request):
        try:
            user_id = request.query_params['user_id']
            user = User.objects.get(pk=user_id)
            user.verified = False
            user.save()
            return JsonResponse({"success": True, "message": "User is no longer verified."})
        except Exception as e:
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
        


class AllSessions(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [CustomAuthentication,]

    def get(self, request):
        try:
            user = request.user
            sessions = user.session_set.all()
            serializedSessions = UserSessionSerializer(sessions,context={"request": request}, many=True).data
            return JsonResponse({"success": True, 'sessions': serializedSessions})
        except Exception as e:
            print(e)
            return JsonResponse({"error": True})
        
    def delete(self, request):
        try:
            user = request.user
            sessions = user.session_set.filter(~Q(session_key=request.session.session_key))
            sessions.delete()
            return JsonResponse({'success': True, 'message': 'Logged out of all but current session'})
        except:
            return JsonResponse({"error": True})
        
        
class SpecificSession(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [CustomAuthentication,]


    def get(self, request):
        try:
            user = request.user
            session_key = request.query_params['session_key']
            session = user.session_set.get(session_key=session_key)
            serializedSession = UserSessionSerializer(session,context={"request": request}).data
            return JsonResponse({"success": True, 'session': serializedSession})
        except Exception as e:
            print(e)
            return JsonResponse({"error": True})

    def delete(self, request):
        try:
            user = request.user
            session_key = request.query_params['session_key']
            session = user.session_set.get(session_key=session_key)
            session.delete()
            return JsonResponse({'success': True, 'message': 'Logged out of session'}, status=200)
        except:
            return JsonResponse({"error": True})
        


@api_view(["DELETE"])
@permission_classes([IsAdmin,])
def delete_all(request):
    User.objects.all().delete()
    return JsonResponse({"success": True}, safe=False)