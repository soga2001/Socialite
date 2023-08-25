from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.utils.html import escape
import json


# From Rest
from rest_framework.views import APIView
from backend.authenticate import *
from .models import BugsReport
from .serializer import BugsReportSerializer
from django.forms import ValidationError

class Bugs(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CustomAuthentication,)

    def post(self, request):
        try:
            user = request.user
            # print(request.body)
            data = json.loads(request.body)
            bug = data['bug']
            replication = data['bug_replication']
            replication = escape(replication)
            bug = escape(bug)
            report = BugsReport(
                user = user,
                bug = bug,
                replication = replication,
            )
            report.save()
            return JsonResponse({'success': True, 'message': 'Bug has been reported'})
        except ValidationError as e:
            return JsonResponse({'error': True, 'message': str(e.message)})
        except Exception as e:
            return JsonResponse({'error': True, 'message': str(e)})
    
    def get(self, request):
        try:
            user = request.user
            reports = BugsReport.objects.filter(user=user)
            serializer = BugsReportSerializer(reports, context={'request': request}, many=True)
            return JsonResponse({'status': 'success', 'message': 'Reported successfully!', 'data': serializer.data})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        

class BugAdminAccess(APIView):
    permission_classes = [IsAdmin, IsAdmin]
    authentication_classes = (CustomAuthentication,)

    def get(self, request):
        try:
            user = request.user
            if user.is_admin:
                reports = BugsReport.objects.all()
                serializer = BugsReportSerializer(reports, many=True)
                return JsonResponse({'status': 'success', 'message': 'Reported successfully!', 'data': serializer.data})
            else:
                return JsonResponse({'status': 'error', 'message': 'You are not an admin!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        
    def put(self, request, id):
        try:
            user = request.user
            if user.is_admin:
                report = BugsReport.objects.get(pk=id)
                report.status = request.POST['status']
                report.save()
                return JsonResponse({'status': 'success', 'message': 'Report updated successfully!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'You are not an admin!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        
    def delete(self, request, id):
        try:
            user = request.user
            if user.is_admin:
                report = BugsReport.objects.get(pk=id)
                report.delete()
                return JsonResponse({'status': 'success', 'message': 'Report deleted successfully!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'You are not an admin!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})