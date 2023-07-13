from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse

from users.models import User
from .serializer import NotificationSerializer

from .models import Notification
from backend.authenticate import *

class NotificationView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CustomAuthentication,)

    def get(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
            notifications = NotificationSerializer(user.notifications.all(), many=True)
            if(notifications):
                # print(notifications.data)
                return JsonResponse({"success": True, "message": "Notifications retrieved", "notifications": notifications.data})
            return JsonResponse({"success": True, "message": "You have no notification."})
        except Exception as e:
            return JsonResponse({"error": True, "message": "An error occured while trying to retrieve notifications. Please try again later."}, safe=False)
        
    def delete(self, request):
        try:
            Notification.objects.filter(recipient=request.user).delete()
            return JsonResponse({"success": True, "message": "Notifications cleared"}, safe=False)
        except Exception as e:
            return JsonResponse({"error": True, "message": "An error occured while trying to clear notifications. Please try again later."}, safe=False)
        

class Mentions(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CustomAuthentication,)

    def get(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
            notifications = NotificationSerializer(user.notifications.filter(verb="mention"), many=True)
            if(notifications):
                return JsonResponse({"success": True, "message": "Mentioned notifications retrieved", "notifications": notifications.data})
            return JsonResponse({"success": True, "message":"You have not been mentioned by any users"})
        except Exception as e:
            return JsonResponse({"error": True, "message": "An error occured while trying to retrieve notification types. Please try again later."}, safe=False)
        
