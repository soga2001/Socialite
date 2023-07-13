from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'notification_room_{self.user_id}'


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

    async def notify_updates(self, event):
        # Handle the "Comment added" message
        message = event['message']
        updateType = event['updateType']
        await self.send(text_data=json.dumps({
            'type': updateType,
            'message': message
        }))
