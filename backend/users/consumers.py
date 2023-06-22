from channels.generic.websocket import AsyncWebsocketConsumer
import json

class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        self.username = self.scope['url_route']['kwargs']['username']
        self.room_group_name = f'user_{self.username}'

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


    async def user_update(self, event):
        # Handle the "Comment added" message
        message = event['message']
        updateType = event['updateType']
        await self.send(text_data=json.dumps({
            'type': updateType,
            'message': message
        }))