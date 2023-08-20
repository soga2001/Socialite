
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
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
channel_layer = get_channel_layer()

from replace import *

# Create your views here.
from notifications.signals import notify

def replace(val):
    u = re.sub(r'@', '', val.group())
    try:
        user = User.objects.get(username=u)
        if user:
            # result = r'<RouterLink :to="{name: `user-profile`, params: {username: {0}}}" :exact="true">@{0}</RouterLink>'.format(u)
            result = '<RouterLink @click.stop="" :to="{name: `user-profile`, params: {username: \'' + u + '\'}}" :exact="true">@' + u + '</RouterLink>'
            return result
            # return r'<a href="/{0}/">@{0}</a>'.format(u)
        else:
            return val
    except User.DoesNotExist:
        return r'{0}'.format(val.group())
    

class Comments(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CustomAuthentication,)

    # id here is post id
    def post(self, request, id):
        try:
            user = request.user
            comment = request.POST['comment']
            comment = escape(comment)
            regex = r'@(\w+)'
            # caption = re.sub(r'@(\w+)', r'<a href="/users/\1/">@\1</a>', caption)
            userlist = []
            comment = re.sub(regex, lambda val: replaceMention(val, userlist), comment)
            comment = replaceLink(comment)

            post = Post.objects.get(pk=id)

            comment = Comment(
                user = user,
                post = post,
                comment = comment
            )
            comment.save()
            
            group_name = f'spill_{id}'
            async_to_sync(channel_layer.group_send)(group_name, {
                "type": "comment.send",
                "message": json.dumps(CommentSerializer(comment, context={'request': request}).data)
            })
            
            link = "{}/spill/{}".format(user.username, id)
            if(user.username in userlist):
                userlist.remove(user.username)
            if(userlist):
                notify.send(user, recipient=userlist, verb='mention', action_object=comment, target=post, description="mentioned you in the comment section", url=link, text=comment.comment)

            if(post.user != request.user):
                notify.send(user, recipient=post.user, verb='commented', action_object=comment, target=post, description="commented on your spill", url=link, text=comment.comment)
            
            return JsonResponse({'status': True, 'message': 'Comment added successfully'})
        except Exception as e:
            return JsonResponse({'status': False, 'message': 'Error adding comment'})

    # id here is post id
    def get(self, request):
        try:
            comments = Comment.objects.filter(user__id=request.user)
            serializer = CommentSerializer(comments, context={'request', request}, many=True)
            return JsonResponse({'status': True, 'message': 'Comments fetched successfully', 'comments': serializer.data})
        except Exception as e:
            return JsonResponse({'status': False, 'message': 'Error fetching comments'})
    
    # id here is comment id    
    def delete(self, request, id):
        try:
            comment = Comment.objects.get(pk=id, user=request.user)
            if comment:
                comment.delete()
                group_name = f'comment_{id}'
                async_to_sync(channel_layer.group_send)(group_name, {
                    "type": "comment.delete",
                    "message": "This comment has been deleted."
                })
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
                group_name = f'comment_{id}'
                async_to_sync(channel_layer.group_send)(group_name, {
                    "type": "comment.update",
                    "message": json.dumps(CommentSerializer(comment, context={'request', request}).data)
                })
                return JsonResponse({'status': True, 'message': 'Comment updated successfully'})
            return JsonResponse({'status': False, 'message': 'Comment not found'})
        except Exception as e:
            return JsonResponse({'status': False, 'message': 'Error updating comment'})


@api_view(["GET"])
def comments_by_post(request, timestamp, page, post_id):
    try:
        comments = Comment.objects.filter(post__id=post_id)
        if(comments):
            serializer = CommentSerializer(comments, context={'request': request}, many=True)
            return JsonResponse({'status': True, 'message': 'Comments fetched successfully', 'comments': serializer.data})
        return JsonResponse({"status": True, "message": 'Post has no comments.'})
    except Exception as e:
        return JsonResponse({'status': False, 'message': 'Error fetching comments'})