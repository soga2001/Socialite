from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse

from users.models import User
from .serializer import NotificationSerializer

from .models import Notification
from backend.authenticate import *
import json



class NotificationView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CustomAuthentication,)

    def get(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
            page = request.query_params['page']
            timestamp = request.query_params['timestamp']
            offset = int(page) * 20
            notif = user.notifications.filter(timestamp__lt=timestamp)[offset:offset+20]
            notifications = NotificationSerializer(notif, context={'request': request}, many=True)
            if(notifications):
                return JsonResponse({"success": True, "message": "Notifications retrieved", "notifications": notifications.data})
            return JsonResponse({"success": True, "message": "You have no notification."})
        except Exception as e:
            print(e)
            return JsonResponse({"error": True, "message": "An error occured while trying to retrieve notifications. Please try again later."}, safe=False)
        
    def delete(self, request):
        try:
            return JsonResponse({"success": True, "message": "Notifications cleared"}, safe=False)
        except Exception as e:
            return JsonResponse({"error": True, "message": "An error occured while trying to clear notifications. Please try again later."}, safe=False)
        
    
class MarkAllAsRead(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CustomAuthentication,)

    def post(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
            user.notifications.filter(unread=True).update(unread=False)
            return JsonResponse({"success": True, "message": "Notifications marked as read"})
        except Exception as e:
            return JsonResponse({"error": True, "message": "An error occured while trying to mark notifications as read. Please try again later."}, safe=False)
        
class MarkAsRead(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CustomAuthentication,)

    def put(self, request):
        try:
            data = json.loads(request.body)
            notification_id = data['id']
            user = User.objects.get(pk=request.user.id)
            user.notifications.filter(pk=notification_id).update(unread=False)
            return JsonResponse({"success": True, "message": "Notification marked as read"})
        except Exception as e:
            return JsonResponse({"error": True, "message": "An error occured while trying to mark notification as read. Please try again later."}, safe=False)

class Mentions(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CustomAuthentication,)

    def get(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
            page = request.query_params['page']
            timestamp = request.query_params['timestamp']
            print(timestamp)
            offset = int(page) * 20
            notifications = NotificationSerializer(user.notifications.filter(verb="mention", timestamp__lt=timestamp)[offset:offset+20], many=True)
            if(notifications):
                return JsonResponse({"success": True, "message": "Mentioned notifications retrieved", "notifications": notifications.data})
            return JsonResponse({"success": True, "message":"You have not been mentioned by any users"})
        except Exception as e:
            print(e)
            return JsonResponse({"error": True, "message": "An error occured while trying to retrieve notification types. Please try again later."}, safe=False)
        


class NotificationsFromFollowedUser(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CustomAuthentication,)

    def post(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
            user.following.filter(followed_user__notification=True).update(notification=False)
            return JsonResponse({"success": True, "message": "Notifications disabled for this user"})
        except Exception as e:
            return JsonResponse({"error": True, "message": "An error occured while trying to disable notifications for this user. Please try again later."}, safe=False)
        
    def delete(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
            user.following.filter(followed_user__notification=False).update(notification=True)
            return JsonResponse({"success": True, "message": "Notifications enabled for this user"})
        except Exception as e:
            return JsonResponse({"error": True, "message": "An error occured while trying to enable notifications for this user. Please try again later."}, safe=False)
        
    
class NotificationsFromUnverifiedUsers(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CustomAuthentication,)

    # enable
    def post(self, request):
        try:
            user = request.user
            user.following.filter(followed_user__verified=False, followed_user__notification=False).update(notification=True)
            return JsonResponse({"success": True, "message": "Notifications enabled for unverified users"})
        except Exception as e:
            return JsonResponse({"error": True, "message": "An error occured while trying to enabling notifications for unverified users. Please try again later."}, safe=False)
        
    # disable
    def delete(self, request):
        try:
            user = request.user
            user.following.filter(followed_user__verified=False, followed_user__notification=True).update(notification=False)
            return JsonResponse({"success": True, "message": "Notifications enabled for this user"})
        except Exception as e:
            return JsonResponse({"error": True, "message": "An error occured while trying to enable notifications for this user. Please try again later."}, safe=False)
        