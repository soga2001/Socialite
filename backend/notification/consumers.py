from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if(self.scope['user'].is_anonymous):
            await self.close()
        else:
            self.user_id = self.scope['user'].id
            self.room_group_name = f'notification_room_{self.user_id}'

            # group add
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

       
    async def disconnect(self, code):
        if hasattr(self, 'room_group_name'):
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