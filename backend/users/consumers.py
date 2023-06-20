from channels.generic.websocket import AsyncWebsocketConsumer
import json

class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'comment_room_{self.user_id}'

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


    async def user_update_send(self, event):
        # Handle the "Comment added" message
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'user_update',
            'message': message
        }))