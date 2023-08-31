from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route'].get('kwargs', {}).get('user_id')
        
        if not self.user_id:
            await self.close()
            return

        self.room_group_name = f'notification_room_{self.user_id}'

        # group add
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def post_update(self, event):
        message = event.get('message')
        updateType = event.get('updateType')
        if message and updateType:
            await self.send(text_data=json.dumps({
                'type': updateType,
                'message': message
            }))