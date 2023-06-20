from channels.generic.websocket import AsyncWebsocketConsumer
import json

class SpillCommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.room_group_name = f'comment_room_{self.post_id}'

        print(self.room_group_name)


        # group add
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )



    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        pass


    async def comment_send(self, event):
        # Handle the "Comment added" message
        print('here')
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'comment',
            'message': message
        }))


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        self.comment_id = self.scope['url_route']['kwargs']['comment_id']
        self.room_group_name = f'comment_{self.comment_id}'

        # group add
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )


    async def disconnect(self, code):
        # group remove
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        pass


    async def comment_update(self, event):
        # Handle the "Comment added" message
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'update',
            'message': message
        }))

    async def comment_delete(self, event):
        # Handle the "Comment added" message
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'delete',
            'message': message
        }))