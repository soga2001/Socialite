# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):

#         self.user_id = self.scope['url_route']['kwargs']['user_id']
#         self.room_group_name = f'notification_room_{self.user_id}'


#         # group add
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#         await self.send({
#             "type": "websocket.accept",
#             "text": 'Hello'
#         })



#     async def disconnect(self, code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#         pass

#     async def websocket_receive(self, event):
#         await self.send({
#             "type": "websocket.send",
#             "text": event["text"],
#         })

#     async def post_update(self, event):
#         message = event['message']
#         print(message)
#         updateType = event['updateType']
#         await self.send(text_data=json.dumps({
#             'type': updateType,
#             'message': message
#         }))

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route'].get('kwargs', {}).get('user_id')
        if not self.user_id:
            # Reject the connection if the user_id is not provided
            await self.close()
            return

        self.room_group_name = f'notification_room_{self.user_id}'

        # group add
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        # await self.send(text_data=json.dumps({
        #     "type": "websocket.accept",
        #     "text": 'Hello'
        # }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def post_update(self, event):
        print(event['message'])
        message = event.get('message')
        print(message)
        updateType = event.get('updateType')
        if message and updateType:
            await self.send(text_data=json.dumps({
                'type': updateType,
                'message': message
            }))
