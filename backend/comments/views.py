
import re
import json
from backend.authenticate import IsAuthenticated, CustomAuthentication
from .models import Comment
from .serializer import CommentSerializer
from posts.models import Post
from users.models import User

# From Django
from django.http import HttpResponse, JsonResponse
from django.utils.html import escape

# From Rest
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes

# Create your views here.


def replace(val):
    u = re.sub(r'@', '', val.group())
    try:
        user = User.objects.get(username=u)
        if user:
            return r'<a href="/profile/user/{0}/">@{0}</a>'.format(u)
        else:
            return val
    except User.DoesNotExist:
        return r'{0}'.format(val.group())
    

class Comments(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CustomAuthentication,)


    # id here is post id
    def post(self, request):
        try:
            user = request.user
            post_id = request.data["post_id"]
            comment = request.data['comment']
            comment = escape(comment)
            regex = r'@(\w+)'
            comment = re.sub(regex, replace, comment)
            comment = Comment(
                user = user,
                post = Post.objects.get(id=post_id),
                comment = comment
            )
            comment.save()
            return JsonResponse({'status': True, 'message': 'Comment added successfully'})
        except Exception as e:
            return JsonResponse({'status': False, 'message': 'Error adding comment'})

    # id here is post id
    def get(self, request, id):
        try:
            comments = Comment.objects.filter(post__id=id)
            serializer = CommentSerializer(comments, many=True)
            return JsonResponse({'status': True, 'message': 'Comments fetched successfully', 'comments': serializer.data})
        except Exception as e:
            return JsonResponse({'status': False, 'message': 'Error fetching comments'})
    
    # id here is comment id    
    def delete(self, request, id):
        try:
            comment = Comment.objects.get(id=id, user=request.user)
            if comment:
                comment.delete()
                return JsonResponse({'status': True, 'message': 'Comment deleted successfully'})
            return JsonResponse({'status': False, 'message': 'Comment not found'})
        except Exception as e:
            return JsonResponse({'status': False, 'message': 'Error deleting comment'})
        
    # id here is comment id
    def put(self, request, id):
        try:
            user = request.user
            comment = Comment.objects.get(id=id, user=request.user)
            newCom = escape(request.POST['comment'])
            if comment:
                comment.comment = newCom
                comment.save()
                return JsonResponse({'status': True, 'message': 'Comment updated successfully'})
            return JsonResponse({'status': False, 'message': 'Comment not found'})
        except Exception as e:
            return JsonResponse({'status': False, 'message': 'Error updating comment'})


@api_view(["GET"])
def comments_by_post(request, timestamp, page, post_id):
    try:
        comments = Comment.objects.filter(post__id=post_id)
        if(comments):
            serializer = CommentSerializer(comments, many=True)
            return JsonResponse({'status': True, 'message': 'Comments fetched successfully', 'data': serializer.data})
        return JsonResponse({"status": True, "message": 'Post has no comments.'})
    except Exception as e:
        return JsonResponse({'status': False, 'message': 'Error fetching comments'})